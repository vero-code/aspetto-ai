import argparse
import logging
from datetime import datetime
from typing import List
import pandas as pd
import utils
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, required=True, help="Path to CSV file")
parser.add_argument("--field", type=str, required=True, help="Field to embed")
parser.add_argument("--db", type=str, default=f"{datetime.now():%Y-%m-%d}", help="MongoDB database name")
parser.add_argument("--coll", type=str, default="embeddings", help="MongoDB collection name")
args = parser.parse_args()

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

    csv_path = os.path.abspath(args.path)
    df = pd.read_csv(csv_path).dropna(subset=[args.field])
    texts = df[args.field].tolist()

    logging.info("🔢 Generating embeddings...")
    df["vector"] = get_embeddings(model, texts)

    logging.info("📦 Inserting into MongoDB...")
    mongo_client = utils.get_mongo_client()
    utils.ingest_data(mongo_client, df, args.db, args.coll)

    logging.info(f"✅ Inserted {len(df)} documents into MongoDB.")

if __name__ == "__main__":
    main()