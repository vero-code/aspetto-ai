# backend/scripts/upload/upload_final_dataset.py

import pandas as pd
import ast
from ..db.connect import get_collection

FINAL_CSV = "data/styles_final.csv"

collection = get_collection()

def main():
    deleted = collection.delete_many({})
    print(f"🗑️ Removed {deleted.deleted_count} old documents")

    df = pd.read_csv(FINAL_CSV)

    items = []
    for _, row in df.iterrows():
        try:
            vector = ast.literal_eval(row["vector"])
        except Exception as e:
            print(f"❌ Error parsing vector: {e}")
            vector = None

        items.append({
            "image_url": row["link"],
            "title": row["productDisplayName"],
            "category": row["articleType"],
            "color": row["baseColour"],
            "gender": row["gender"],
            "style_tags": [row["usage"], row["season"]],
            "vector": vector,
            "source": "dataset"
        })

    collection.insert_many(items)
    print(f"✅ Uploaded {len(items)} documents to MongoDB")

if __name__ == "__main__":
    main()
