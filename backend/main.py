from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
from utils import suggest_unique_images,get_similar_images_by_id,check_collection_exists,restore_qdrant_collection
from qdrant_client import QdrantClient
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from logger import logger

import os
from dotenv import load_dotenv
load_dotenv()


client = QdrantClient(url=os.getenv("QDRANT_URL"),api_key=os.getenv("QDRANT_API_KEY"))


# Lifespan event to restore qdrant collection if do not exist on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    collection_name = os.getenv("QDRANT_COLLECTION_NAME")
    if(not check_collection_exists(client,collection_name)):
        logger.info("Restoring Qdrant snapshot file")
        if(os.path.exists('./data/fashion_products_vdb.snapshot')):
            logger.error("Snapshot file not found! Please upload to ./data/fashion_products_vdb.snapshot")
        restore_qdrant_collection(
            qdrant_url=os.getenv("QDRANT_URL"),
            collection_name=collection_name,
            api_key=os.getenv("QDRANT_API_KEY"),
            snapshot_file_path='./data/fashion_products_vdb.snapshot'
        )
    yield



app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    


@app.get("/get-products/")
async def get_products(collection_name: str,top_k:int):
    result=suggest_unique_images(client, collection_name, top_k=top_k)
    return JSONResponse(content=result['content'], status_code=result['status_code'])

@app.get("/get-recommendations/")
def get_recomendations(image_id:str,collection_name: str,top_k:int,page:int=0):
    result=get_similar_images_by_id(client, collection_name, image_id, top_k=top_k,page=page)
    return JSONResponse(content=result['content'], status_code=result['status_code'])
