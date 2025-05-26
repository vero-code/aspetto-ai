# backend/scripts/db/connect.py

import logging
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

class ClientError(Exception):
    pass

class DataError(Exception):
    pass

def get_collection(db_name: str = None, coll_name: str = None):
    """
    Gets a MongoDB collection object.
    If db_name is not specified, the value from the MONGO_DB_NAME environment variable is used.
    """
    db = get_db(get_mongo_client(), db_name)
    if coll_name is None:
        coll_name = os.getenv("MONGO_COLL_NAME", "fashion_items")
    return db[coll_name]

def get_db(client, db_name: str = None):
    """
    Gets a MongoDB database object.
    If db_name is not specified, the value from the MONGO_DB_NAME environment variable is used.
    """
    if db_name is None:
        db_name = os.getenv("MONGO_DB_NAME", "aspetto_db")
    return client[db_name]

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
