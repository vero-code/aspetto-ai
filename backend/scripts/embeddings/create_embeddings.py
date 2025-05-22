import argparse
import logging
from datetime import datetime
from typing import List
import cohere
import pandas as pd
import utils
from tqdm import tqdm
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, required=True, help="Path to CSV file")
parser.add_argument("--field", type=str, required=True, help="Field to embed")
parser.add_argument("--db", type=str, default=f"{datetime.now():%Y-%m-%d}", help="MongoDB database name")
parser.add_argument("--coll", type=str, default="embeddings", help="MongoDB collection name")
args = parser.parse_args()

def get_embeddings(client: cohere.Client, texts: List[str]) -> List[List[float]]:
    embeddings = []
    for i in tqdm(range(0, len(texts), 128)):
        batch = texts[i:i+128]
        result = client.embed(texts=batch, model="embed-english-v3.0", input_type="search_document")
        embeddings.extend(result.embeddings)
    return embeddings

def main():
    cohere_key = utils.get_cohere_api_key()
    client = cohere.Client(cohere_key)

    csv_path = os.path.abspath(args.path)
    df = pd.read_csv(csv_path).dropna(subset=[args.field])
    texts = df[args.field].tolist()

    logging.info("🔢 Generating embeddings...")
    df["embeddings"] = get_embeddings(client, texts)

    logging.info("📦 Inserting into MongoDB...")
    mongo_client = utils.get_mongo_client()
    utils.ingest_data(mongo_client, df, args.db, args.coll)

    logging.info(f"✅ Inserted {len(df)} documents into MongoDB.")

if __name__ == "__main__":
    main()