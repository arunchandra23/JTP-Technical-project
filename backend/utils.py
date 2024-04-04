import os
import cv2
import numpy as np
import pandas as pd
from skimage.feature import local_binary_pattern
from concurrent.futures import ProcessPoolExecutor
from qdrant_client.http import models
import uuid as uuidpy

def compute_color_histogram(image, bins=32):
    hist = [cv2.calcHist([image], [i], None, [bins], [0, 256]) for i in range(3)]
    hist = np.concatenate(hist).flatten()
    hist = hist / hist.sum()
    return hist

def compute_texture_features(image, radius=3, n_points=24):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lbp = local_binary_pattern(gray_image, n_points, radius, method='uniform')
    lbp_hist, _ = np.histogram(lbp, bins=np.arange(0, n_points + 3), range=(0, n_points + 2))
    lbp_hist = lbp_hist / lbp_hist.sum()
    return lbp_hist

def compute_edge_features(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=5)
    edges = np.sqrt(sobelx ** 2 + sobely ** 2)
    edge_hist, _ = np.histogram(edges, bins=32, range=(0, 256))
    edge_hist = edge_hist / edge_hist.sum()
    return edge_hist

def compute_feature_vector(image_path):
    image=cv2.imread(image_path)
    color_features = compute_color_histogram(image)
    texture_features = compute_texture_features(image)
    edge_features = compute_edge_features(image)
    feature_vector = np.concatenate([color_features*2, texture_features, edge_features*3])
    # print("FV>>",len(feature_vector))
    return feature_vector

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
def store_embeddings_in_qdrant(client, collection_name, image_files, feature_vectors):
    points = []
    for img_path, feature_vector in zip(image_files, feature_vectors):
        payload = {"image_path": img_path}
        points.append(models.PointStruct(
            id=str(uuidpy.uuid4()),
            vector=feature_vector.tolist(),
            payload=payload
        ))

    client.upsert(
        collection_name=collection_name,
        points=points,
        wait=True
    )
def find_similar_images_in_qdrant_v1(client, collection_name, input_image, top_k=2):
    input_features = compute_feature_vector(input_image)

    # input_reduced_features = input_features
    search_result = client.search(
        collection_name=collection_name,
        query_vector=input_features.tolist(),
        query_filter=None,
        limit=top_k,
    )
    print("SR>>",search_result)
    similar_images = []
    for hit in search_result:
        similar_images.append(hit.payload["image_path"])
    return similar_images
def find_similar_images_in_qdrant(client, collection_name, input_image, top_k=2):
    input_features = compute_feature_vector(input_image)

    # input_reduced_features = input_features
    search_result = client.search(
        collection_name=collection_name,
        query_vector=input_features.tolist(),
        query_filter=None,
        limit=top_k,
    )
    print("SR>>",search_result)
    similar_images = []
    for hit in search_result:
        similar_images.append({"filename":hit.payload['filename'], "url":hit.payload['url']})
    return similar_images


def compute_feature_vectors_parallel(image_dataset, max_workers=None):
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        feature_vectors = list(executor.map(compute_feature_vector, image_dataset))
    return feature_vectors


def process_image(image_detail):
    # Wrapper function for processing a single image
    # Returns a tuple containing the image_path and its feature_vector
    feature_vector = compute_feature_vector(image_detail['image_path'])
    return (image_detail, feature_vector)

def process_and_store_images_parallel(dataset_path,client, collection_name, vector_dim,csv_path, max_workers=None):
    # Ensure the collection exists or create it if not
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
            

# ==========================================
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model

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

def compute_feature_vector_v2(image_path):
    

    # Load the saved encoder model
    loaded_encoder = load_model('/media/arunchandra/local/personal/JTP-Technical-project/backend/data/encoder_model_test_train_2ep.h5')
    
    return extract_embeddings([image_path], loaded_encoder, target_size=(32, 32))[0]

def process_image_v2(image_detail):
    # Wrapper function for processing a single image
    # Returns a tuple containing the image_path and its feature_vector
    print("IP>>",image_detail['image_path'])
    feature_vector = compute_feature_vector_v2(image_detail['image_path'])
    return (image_detail, feature_vector)

def process_and_store_images_parallel_v2(dataset_path,client, collection_name, vector_dim,csv_path, max_workers=None):
    # Ensure the collection exists or create it if not
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
        for image_detail, feature_vector in executor.map(process_image_v2, image_details):
            store_single_embedding_in_qdrant(client, collection_name, image_detail, feature_vector)

def find_similar_images_in_qdrant_v2(client, collection_name, input_image, top_k=2):
    loaded_encoder = load_model('/media/arunchandra/local/personal/JTP-Technical-project/backend/data/encoder_model_test_train_2ep.h5')

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