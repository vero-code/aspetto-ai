import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["aspetto_db"]
collection = db["fashion_items"]

deleted = collection.delete_many({})
print(f"🗑️ Old documents removed: {deleted.deleted_count}")

styles_df = pd.read_csv("data/styles_clean.csv")
images_df = pd.read_csv("data/images.csv")

images_df["id"] = images_df["filename"].str.replace(".jpg", "", regex=False).astype(int)
merged_df = pd.merge(styles_df, images_df, on="id")

merged_df = merged_df.head(1000)

items = []
for _, row in merged_df.iterrows():
    items.append({
        "image_url": row["link"],
        "title": row["productDisplayName"],
        "category": row["articleType"],
        "color": row["baseColour"],
        "gender": row["gender"],
        "style_tags": [row["usage"], row["season"]],
        "vector": None,
        "source": "dataset"
    })

collection.insert_many(items)
print(f"✅ Loaded {len(items)} documents into MongoDB.")