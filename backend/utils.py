import os
import shlex
import subprocess
import json
import random
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from qdrant_client.http import models
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import uuid as uuidpy
from logger import logger





def check_collection_exists(client, collection_name):
    """
    Checks if a collection exists in the Qdrant server.

    Parameters:
    - client: The Qdrant client instance.
    - collection_name: The name of the collection to check.

    Returns:
    - True if the collection exists, False otherwise.
    """
    try:
        client.get_collection(collection_name)
        return True
    except Exception as e:    
        return False


def call_curl(curl):
    """
    Executes a cURL command and returns the JSON output.

    Parameters:
    - curl: The cURL command as a string.

    Returns:
    - The JSON output of the cURL command.
    """
    args = shlex.split(curl)
    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return json.loads(stdout.decode('utf-8'))


def restore_qdrant_collection(qdrant_url, collection_name, api_key, snapshot_file_path):
    """
    Restore a Qdrant collection from a snapshot file.

    Parameters:
    - qdrant_url: The URL of the Qdrant server.
    - collection_name: The name of the collection to restore.
    - api_key: API key for Qdrant authentication.
    - snapshot_file_path: The file path to the snapshot file.
    """
    try:
        snapshot_file_path = os.path.abspath(snapshot_file_path)
        cu=f"""curl -X POST '{qdrant_url}/collections/{collection_name}/snapshots/upload?priority=snapshot' \
        -H 'api-key: {api_key}' \
        -H 'Content-Type:multipart/form-data' \
        -F 'snapshot=@{snapshot_file_path}'"""
        output = call_curl(cu)
        logger.info(output)
    except Exception as e:
        logger.error(f"Failed to restore collection '{collection_name}', please check Qdrant. Error: {e}")
    

def create_qdrant_collection(client, collection_name, vector_dim):
    """
    Creates a new collection in Qdrant with the specified vector dimension.

    Parameters:
    - client: The Qdrant client instance.
    - collection_name: The name of the collection to create.
    - vector_dim: The dimension of the vectors to be stored in the collection.
    """
    try:
        if(not check_collection_exists(client=client,collection_name=collection_name)):
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=vector_dim, distance=models.Distance.COSINE),
            )
            logger.info(f"Collection {collection_name} created successfully")
            return
        logger.info(f"Collection {collection_name} already exists")
        
        
    except Exception as e:
        logger.error(f"Failed to create collection '{collection_name}'. Error: {e}")


def store_single_embedding_in_qdrant(client, collection_name, image_detail, feature_vector):
    """
    Stores a single image embedding in a Qdrant collection.

    Parameters:
    - client: The Qdrant client instance.
    - collection_name: The name of the collection where the embedding will be stored.
    - image_detail: A dictionary containing details about the image.
    - feature_vector: The feature vector representing the image.
    """
    # Create a payload with the image path
    payload = { "filename":image_detail['filename'], "url":image_detail['url'],"gender":image_detail['gender'],"masterCategory":image_detail['masterCategory'],"subCategory":image_detail['subCategory'],"articleType":image_detail['articleType'],"baseColour":image_detail['baseColour'],"season":image_detail['season'],"year":image_detail['year'],"usage":image_detail['usage'],"productDisplayName":image_detail['productDisplayName']}
    # Generate a unique ID for the point
    point_id = str(uuidpy.uuid4())
    # Create the point structure
    point = models.PointStruct(id=point_id, vector=feature_vector.tolist(), payload=payload)
    # Insert the point into the collection
    client.upsert(collection_name=collection_name, points=[point], wait=True)
    logger.info(f"Stored embedding for image '{image_detail['image_path']}' in the collection '{collection_name}'.")


def preprocess_image(image_path, target_size):
    """
    Preprocesses an image for input into a neural network.

    Parameters:
    - image_path: The path to the image file.
    - target_size: The target size for the image (width, height).

    Returns:
    - The preprocessed image as a numpy array.
    """
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
    """
    Extracts embeddings for a list of images using a given encoder.

    Parameters:
    - image_paths: A list of paths to image files.
    - encoder: The encoder model to use for extracting embeddings.
    - target_size: The target size for the images (width, height).

    Returns:
    - A numpy array containing the embeddings for the input images.
    """
    embeddings = []
    for image_path in image_paths:
        preprocessed_image = preprocess_image(image_path, target_size=target_size)
        embedding = encoder.predict(preprocessed_image)
        embeddings.append(embedding.flatten())  # Flatten the embedding to a 1D vector
    return np.array(embeddings)


def compute_feature_vector(image_path):
    """
    Computes the feature vector for a single image using a pre-trained encoder from path in the environment variable.

    Parameters:
    - image_path: The path to the image file.

    Returns:
    - The feature vector representing the image.
    """
    # Load the saved encoder model
    loaded_encoder = load_model(os.getenv('ENCODER_MODEL_PATH'))
    return extract_embeddings([image_path], loaded_encoder, target_size=(32, 32))[0]


def process_image(image_detail):
    """
    Wrapper function for processing a single image and returns its details and feature vector.

    Parameters:
    - image_detail: A dictionary containing details about the image.

    Returns:
    - A tuple containing the image details and its feature vector.
    """
    # Wrapper function for processing a single image
    # Returns a tuple containing the image_path and its feature_vector
    logger.info(f"IP>>{image_detail['image_path']}")
    feature_vector = compute_feature_vector(image_detail['image_path'])
    return (image_detail, feature_vector)


def process_and_store_images_parallel(dataset_path,client, collection_name, vector_dim,csv_path, max_workers=None):
    """
    Processes and stores images in a Qdrant collection in parallel.

    Parameters:
    - dataset_path: The path to the dataset directory.
    - client: The Qdrant client instance.
    - collection_name: The name of the collection where embeddings will be stored.
    - vector_dim: The dimension of the vectors to be stored in the collection.
    - csv_path: The path to the CSV file containing image details.
    - max_workers: The maximum number of worker processes to use (default is None).
    """
    create_qdrant_collection(client, collection_name, vector_dim)
    # Read the csv file containing image details and urls
    image_details=[]
    csv=pd.read_csv(csv_path)
    print(csv.head())
    for row in csv.iterrows():
        image_path=os.path.join(dataset_path,row[1]['filename'])
        if(os.path.exists(image_path)):
            detail={}
            detail['image_path']=image_path
            detail['filename']=row[1]['filename']
            detail['url']=row[1]['link']
            detail['gender']=row[1]['gender']
            detail['masterCategory']=row[1]['masterCategory']
            detail['subCategory']=row[1]['subCategory']
            detail['articleType']=row[1]['articleType']
            detail['baseColour']=row[1]['baseColour']
            detail['season']=row[1]['season']
            detail['year']=row[1]['year']
            detail['usage']=row[1]['usage']
            detail['productDisplayName']=row[1]['productDisplayName']
            image_details.append(detail)
    # Process images in parallel to compute feature vectors
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for image_detail, feature_vector in executor.map(process_image, image_details):
            store_single_embedding_in_qdrant(client, collection_name, image_detail, feature_vector)



def qdrant_payload_as_dict(points):
    """
    Converts Qdrant point payloads to a list of dictionaries.

    Parameters:
    - points: A list of Qdrant points.

    Returns:
    - A list of dictionaries containing payload data.
    """
    payloads=[]
    for point in points:
        payloads.append({
            'id': point.id, 
            'url': point.payload.get('url'),
            'productDisplayName': point.payload.get('productDisplayName'),
            'gender': point.payload.get('gender'),
            'baseColour': point.payload.get('baseColour'),
            'masterCategory': point.payload.get('masterCategory'),
            'subCategory': point.payload.get('subCategory'),
            'articleType': point.payload.get('articleType'),
            'season': point.payload.get('season'),
            'usage': point.payload.get('usage'),
            })
    return payloads
     
         
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
    try:
        # Fetch all point IDs (or a large sample) from the collection
        search_result = client.scroll(collection_name=collection_name, limit=10000)
        points = search_result[0]
        
        # Randomly select point IDs without replacement to ensure uniqueness
        selected_points = random.sample(points, min(top_k, len(points)))
        
        # Extract the image_path and other relevant info from the selected points
        suggested_images = qdrant_payload_as_dict(selected_points)
        return {'content':suggested_images,'status_code':200}
    except Exception as e:
        logger.error(f"Failed to suggest unique images from collection '{collection_name}'. Error: {e}")
        return {'content':[],'status_code':400}


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
    try:
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
            limit=top_k+1,
            offset = page * top_k+1
        )
        if(len(search_results)!=0):
            if(search_results[0].id==image_id):
                search_results.pop(0)
        # Extract the IDs and payload of the similar images
        similar_images = qdrant_payload_as_dict(search_results[:top_k])
        
        return {'content':similar_images,'status_code':200}
    except Exception as e:
        logger.error(f"Failed to retrieve similar images for ID '{image_id}' from collection '{collection_name}'. Error: {e}")
        return {'content':[],'status_code':400}

