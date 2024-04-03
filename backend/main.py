from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import shutil
from utils import find_similar_images_in_qdrant
from qdrant_client import QdrantClient

import os
from dotenv import load_dotenv
load_dotenv()



app=FastAPI()

client = QdrantClient(url=os.getenv("QDRANT_URL"),api_key=os.getenv("QDRANT_API_KEY"))
collection_name = "image_collection_final"



@app.post("/get-recommendation")
async def get_recommendation():
    return {"message": "Hello World"}

@app.post("/find-similar-images/")
async def find_similar_images(collection_name: str,top_k:int, file: UploadFile = File(...)):
    # Save uploaded image to a temporary file
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        similar_images = find_similar_images_in_qdrant(client, collection_name, temp_file_path, top_k=top_k)
    finally:
        os.remove(temp_file_path)
    
    return JSONResponse(content={"similar_images": similar_images})