import argparse
from utils import process_and_store_images_parallel
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os
load_dotenv()
def main(args):
    
    try:
        client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY'))

        vector_dim = 154  # Total dimension of concatenated feature vectors
        process_and_store_images_parallel(args.dataset_path,client, args.collection_name, vector_dim,args.csv_path, max_workers=None)
        print(f"Stored embeddings for images in the collection '{args.collection_name}'.")
        
    except Exception as e:
        print(f"Failed to store embeddings in the collection '{args.collection_name}'.")
        print(e)
        return None
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Used to create and store image embeddings in a Qdrant collection.')
    parser.add_argument('collection_name', type=str, help='Name of the Qdrant collection.')
    parser.add_argument('dataset_path', type=str, help='Path to the folder containing images.',default="./data/images/")
    parser.add_argument('csv_path', type=str, help='Path to the csv file containing image details.',default="./data/image_details.csv")

    args = parser.parse_args()

    main(args)
