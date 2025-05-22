import logging
import cohere
import pandas as pd
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

class ClientError(Exception):
    pass

class DataError(Exception):
    pass

def get_cohere_api_key() -> str:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ClientError("❌ COHERE_API_KEY is not set in the environment.")
    return api_key

def get_cohere_client() -> cohere.Client:
    api_key = get_cohere_api_key()
    client = cohere.Client(api_key)
    try:
        client.tokenize("ping")
        logging.info("✅ Cohere client authenticated.")
        return client
    except cohere.error.CohereAPIError:
        logging.error("❌ Cohere authentication failed.")
        raise ClientError("Invalid Cohere API key.")

def get_mongo_client() -> pymongo.MongoClient:
    try:
        client = pymongo.MongoClient(get_mongo_uri())
        logging.info("✅ Connected to MongoDB.")
        return client
    except pymongo.errors.ConnectionFailure as e:
        logging.error("❌ MongoDB connection failed.")
        raise ClientError(e)

def get_mongo_uri() -> str:
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ClientError("❌ MONGO_URI is not set in the environment.")
    
    return mongo_uri

def ingest_data(
    client: pymongo.MongoClient, data: pd.DataFrame, db: str, coll: str
) -> None:
    collection = client[db][coll]
    collection.drop()
    collection.insert_many(data.to_dict("records"))
    logging.info(f"📥 Inserted {len(data)} documents into {db}.{coll}")