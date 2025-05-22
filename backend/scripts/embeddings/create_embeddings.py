import logging
from typing import List
import utils
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

DB_NAME = "aspetto_db"
COLL_NAME = "fashion_items"
FIELD_TO_EMBED = "title"

def get_embeddings(model: SentenceTransformer, texts: List[str]) -> List[List[float]]:
    embeddings = []
    for i in tqdm(range(0, len(texts), 128)):
        batch = texts[i:i+128]
        batch_embeddings = model.encode(batch, show_progress_bar=False).tolist()
        embeddings.extend(batch_embeddings)
    return embeddings

def main():
    logging.info("⚙️ Loading embedding model from Hugging Face...")
    model = SentenceTransformer("thenlper/gte-small")

    logging.info("📦 Connecting to MongoDB...")
    mongo_client = utils.get_mongo_client()
    mongo_collection = mongo_client[DB_NAME][COLL_NAME]

    logging.info("📄 Fetching documents without vector...")
    docs = list(mongo_collection.find({FIELD_TO_EMBED: {"$exists": True}, "vector": None}))
    if not docs:
        logging.info("✅ No documents to update. All have vectors.")
        return
    
    texts = [doc[FIELD_TO_EMBED] for doc in docs]
    ids = [doc["_id"] for doc in docs]

    logging.info("🔢 Generating embeddings...")
    vectors = get_embeddings(model, texts)

    logging.info("📝 Updating documents in MongoDB...")
    for _id, vector in zip(ids, vectors):
        mongo_collection.update_one({"_id": _id}, {"$set": {"vector": vector}})

    logging.info(f"✅ Updated {len(vectors)} documents with vector embeddings.")

if __name__ == "__main__":
    main()