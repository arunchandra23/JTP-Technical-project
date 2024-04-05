import os
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from qdrant_client.http import models
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import uuid as uuidpy


def create_qdrant_collection(client, collection_name, vector_dim):
    try:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=vector_dim, distance=models.Distance.COSINE),
        )
    except Exception as e:
        print(f"Failed to create collection '{collection_name}'.")
        print(e)


def store_single_embedding_in_qdrant(client, collection_name, image_detail, feature_vector):
    # Create a payload with the image path
    payload = { "filename":image_detail['filename'], "url":image_detail['url']}
    # Generate a unique ID for the point
    point_id = str(uuidpy.uuid4())
    # Create the point structure
    point = models.PointStruct(id=point_id, vector=feature_vector.tolist(), payload=payload)
    # Insert the point into the collection
    client.upsert(collection_name=collection_name, points=[point], wait=True)
    print(f"Stored embedding for image '{image_detail['image_path']}' in the collection '{collection_name}'.")


def preprocess_image(image_path, target_size):
    # Load the image
    img = image.load_img(image_path, target_size=target_size, color_mode='rgb')
    # Convert the image to a numpy array
    img_array = image.img_to_array(img)
    # Rescale the image
    img_array = img_array / 255.0
    # Expand dimensions to match the input shape of the encoder
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def extract_embeddings(image_paths, encoder, target_size):
    embeddings = []
    for image_path in image_paths:
        preprocessed_image = preprocess_image(image_path, target_size=target_size)
        embedding = encoder.predict(preprocessed_image)
        embeddings.append(embedding.flatten())  # Flatten the embedding to a 1D vector
    return np.array(embeddings)

def compute_feature_vector(image_path):

    # Load the saved encoder model
    loaded_encoder = load_model(os.getenv('ENCODER_MODEL_PATH'))
    
    return extract_embeddings([image_path], loaded_encoder, target_size=(32, 32))[0]

def process_image(image_detail):
    # Wrapper function for processing a single image
    # Returns a tuple containing the image_path and its feature_vector
    print("IP>>",image_detail['image_path'])
    feature_vector = compute_feature_vector(image_detail['image_path'])
    return (image_detail, feature_vector)

def process_and_store_images_parallel(dataset_path,client, collection_name, vector_dim,csv_path, max_workers=None):
    create_qdrant_collection(client, collection_name, vector_dim)
    
    # Read the csv file containing image details and urls
    image_details=[]
    csv=pd.read_csv(csv_path)
    for row in csv.iterrows():
        image_path=dataset_path+row[1]['filename']
        if(os.path.exists(image_path)):
            detail={}
            detail['image_path']=image_path
            detail['filename']=row[1]['filename']
            detail['url']=row[1]['link']
            image_details.append(detail)
    # Process images in parallel to compute feature vectors
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for image_detail, feature_vector in executor.map(process_image, image_details):
            store_single_embedding_in_qdrant(client, collection_name, image_detail, feature_vector)

def find_similar_images_in_qdrant(client, collection_name, input_image, top_k=2):
    loaded_encoder = load_model(os.getenv('ENCODER_MODEL_PATH'))

    input_embedding = extract_embeddings([input_image], loaded_encoder, target_size=(32, 32))[0]

    # input_reduced_features = input_features
    search_result = client.search(
        collection_name=collection_name,
        query_vector=input_embedding,
        query_filter=None,
        limit=top_k,
    )
    print("SR>>",search_result)
    similar_images = []
    for hit in search_result:
        similar_images.append({"filename":hit.payload['filename'], "url":hit.payload['url']})
    return similar_images

import random

def suggest_unique_images(client, collection_name, top_k=20):
    """
    Suggests a random sample of unique images from a Qdrant collection.
    
    Args:
    - client (QdrantClient): The Qdrant client.
    - collection_name (str): The name of the collection to query.
    - sample_size (int): The number of unique images to suggest.
    
    Returns:
    - list of dict: A list of dictionaries, each containing the 'id' and 'image_path' of the suggested images.
    """
    # Fetch all point IDs (or a large sample) from the collection
    search_result = client.scroll(collection_name=collection_name, limit=10000)
    points = search_result[0]
    
    # Randomly select point IDs without replacement to ensure uniqueness
    selected_points = random.sample(points, min(top_k, len(points)))
    
    # Extract the image_path and other relevant info from the selected points
    suggested_images = [{'id': point.id, 'url': point.payload.get('url')} for point in selected_points]
    
    return suggested_images


def get_similar_images_by_id(client, collection_name, image_id, top_k=5,page=0):
    """
    Retrieves similar images to the given image ID from a Qdrant collection.
    
    Args:
    - client (QdrantClient): The Qdrant client instance.
    - collection_name (str): The name of the collection where images are stored.
    - image_id (str): The ID of the image to find similarities for.
    - top_k (int): The number of similar images to retrieve.
    
    Returns:
    - list: A list of similar image IDs, excluding the original image ID.
    """
    # Fetch the vector of the specified image ID
    point = client.retrieve(
    collection_name=f"{collection_name}",
    ids=[image_id],
    with_vectors=True
    )
    if len(point)==0:
        return []  # Return an empty list if the image ID is not found
    point=point[0]
    query_vector = point.vector
    
    # Search for similar images using the vector of the given image ID
    search_results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        query_filter=models.Filter(must_not=[models.FieldCondition(
            key="id",
                match=models.MatchValue(
                    value=image_id,
                    )
            )]), 
        limit=top_k,
        offset = page * top_k
    )
    
    # Extract the IDs and Urls of the similar images
    similar_image_ids = [{"id":hit.id,"url":hit.payload['url']} for hit in search_results]
    
    return similar_image_ids


