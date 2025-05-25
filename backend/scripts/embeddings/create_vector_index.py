# backend/scripts/embeddings/create_vector_index.py

from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
collection = client["aspetto_db"]["fashion_items"]

search_index_model = SearchIndexModel(
    definition={
        "fields": [
            {
                "type": "vector",
                "path": "vector",
                "numDimensions": 384,
                "similarity": "cosine",
                "datatype": "float32"
            }
        ]
    },
    name="vector_index",
    type="vectorSearch"
)

collection.create_search_index(model=search_index_model)
print("✅ Vector index created or updated.")