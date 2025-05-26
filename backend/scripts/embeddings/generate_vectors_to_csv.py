# backend/scripts/embeddings/generate_vectors_to_csv.py

import pandas as pd
from sentence_transformers import SentenceTransformer
import logging
from build_text import build_text_from_row

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

INPUT_CSV = "data/styles_clean.csv"
OUTPUT_CSV = "data/styles_with_vectors.csv"

model = SentenceTransformer("thenlper/gte-small")

def main():
    df = pd.read_csv(INPUT_CSV)
    logging.info(f"📄 Loaded {len(df)} rows from {INPUT_CSV}")

    texts = df.apply(lambda row: build_text_from_row(row.to_dict()), axis=1)

    logging.info("🧠 Generating embeddings...")
    vectors = model.encode(texts.tolist(), show_progress_bar=True)

    df["vector"] = [str(v.tolist()) for v in vectors]

    df.to_csv(OUTPUT_CSV, index=False)
    logging.info(f"✅ Saved with vectors to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
