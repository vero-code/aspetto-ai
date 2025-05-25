# backend/scripts/embeddings/create_embeddings.py

import logging
import utils
from tqdm import tqdm
from build_text import build_text_for_embedding
from vector_utils import get_embeddings

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

DB_NAME = "aspetto_db"
COLL_NAME = "fashion_items"

def main():
    logging.info("📦 Connecting to MongoDB...")
    mongo_client = utils.get_mongo_client()
    mongo_collection = mongo_client[DB_NAME][COLL_NAME]

    logging.info("📄 Fetching documents without vector...")
    docs = list(mongo_collection.find({
        "title": {"$exists": True},
        "vector": None
    }))

    if not docs:
        logging.info("✅ No documents to update. All have vectors.")
        return
    
    texts = [build_text_for_embedding(doc) for doc in docs]
    ids = [doc["_id"] for doc in docs]

    logging.info("🔢 Generating embeddings...")
    compressed_vectors = get_embeddings(texts)

    logging.info("📝 Updating documents in MongoDB...")
    for _id, vector in tqdm(zip(ids, compressed_vectors), total=len(ids)):
        mongo_collection.update_one({"_id": _id}, {"$set": {"vector": vector}})

    logging.info(f"✅ Updated {len(compressed_vectors)} documents with compressed vector embeddings.")

if __name__ == "__main__":
    main()