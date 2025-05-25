# backend/scripts/embeddings/create_embeddings.py
import logging
from typing import List
import utils
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import struct
from bson.binary import Binary

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

DB_NAME = "aspetto_db"
COLL_NAME = "fashion_items"

model = SentenceTransformer("thenlper/gte-small")

def compress_vector(vector: List[float]) -> Binary:
    """
    Convert a list of float32 into BSON binary format for efficient storage.
    """
    float_bytes = struct.pack(f"<{len(vector)}f", *vector)
    return Binary(float_bytes, subtype=0x0A)

def get_embeddings(texts: List[str]) -> List[Binary]:
    """
    Generates embeddings and returns them in BSON binary format.
    """
    compressed = []
    for i in tqdm(range(0, len(texts), 128)):
        batch = texts[i:i+128]
        vectors = model.encode(batch, show_progress_bar=False)
        compressed.extend([compress_vector(vec) for vec in vectors])
    return compressed

def build_text_for_embedding(doc: dict) -> str:
    """
    Assembles a text string from document fields to generate an embedding.
    """
    parts = [
        doc.get("title", ""),
        doc.get("category", ""),
        doc.get("color", ""),
        doc.get("gender", ""),
        ", ".join(str(tag) for tag in doc.get("style_tags", []))
    ]

    for part in parts:
        if not isinstance(part, str):
            print("⚠️ Non-string part:", part, type(part))

    return " | ".join(str(part) for part in parts if part)

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
    for _id, vector in zip(ids, compressed_vectors):
        mongo_collection.update_one({"_id": _id}, {"$set": {"vector": vector}})

    logging.info(f"✅ Updated {len(compressed_vectors)} documents with compressed vector embeddings.")

if __name__ == "__main__":
    main()