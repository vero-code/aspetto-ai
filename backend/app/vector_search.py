# backend/app/vector_search.py
from app.mongodb import collection

def search_similar_items(vector: list[float], limit: int = 5) -> list[dict]:
    """Searches for similar fashion items in MongoDB using vector search."""
    print("🔍 Searching MongoDB for similar items...")

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": vector,
                "path": "vector",
                "numCandidates": 100,
                "limit": limit,
                "index": "vector_index"
            }
        },
        {
            "$project": {
                "title": 1,
                "image_url": 1,
                "style_tags": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ])

    similar_items = list(results)
    print(f"✅ Found {len(similar_items)} similar items.")
    return similar_items
