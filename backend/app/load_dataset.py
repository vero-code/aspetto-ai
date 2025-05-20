import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["aspetto_db"]
collection = db["fashion_items"]

df = pd.read_csv("data/fashion_sample.csv")

items = []
for _, row in df.iterrows():
    items.append({
        "image_url": row["imageURL"],
        "title": row["productDisplayName"],
        "category": row["articleType"],
        "color": row["baseColour"],
        "gender": row["gender"],
        "style_tags": [row["usage"], row["season"]],
        "vector": None
    })

collection.insert_many(items)
print(f"✅ Loaded {len(items)} documents into MongoDB.")