from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import shutil
from utils import find_similar_images_in_qdrant, find_similar_images_in_qdrant_v1,find_similar_images_in_qdrant_v2,suggest_unique_images,get_similar_images_by_id
from qdrant_client import QdrantClient
from starlette.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv
load_dotenv()



app=FastAPI()


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        # similar_images = find_similar_images_in_qdrant_v1(client, collection_name, temp_file_path, top_k=top_k)
        # similar_images = find_similar_images_in_qdrant(client, collection_name, temp_file_path, top_k=top_k)
        similar_images = find_similar_images_in_qdrant_v2(client, collection_name, temp_file_path, top_k=top_k)
    finally:
        os.remove(temp_file_path)
    
    return JSONResponse(content=similar_images)

@app.get("/get-products/")
async def get_products(collection_name: str,top_k:int):
    result=suggest_unique_images(client, collection_name, top_k=top_k)
    return JSONResponse(content=result)

@app.get("/get-recommendations/")
def get_recomendations(image_id:str,collection_name: str,top_k:int,page:int=0):
    result=get_similar_images_by_id(client, collection_name, image_id, top_k=top_k,page=page)
    return JSONResponse(content=result)