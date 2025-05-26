# backend/app/services/vector_search.py

from scripts.db.connect import get_collection
from typing import Optional

def search_similar_items(
    vector: list[float],
    limit: int = 3,
    category: Optional[str] = None,
    color: Optional[str] = None,
    gender: Optional[str] = None
) -> list[dict]:
    """Searches for similar fashion items in MongoDB using vector search with optional filters."""
    print("🔍 Searching MongoDB for similar items...")

    # Try stricter filter first
    priority_filters = [
        {"category": category, "color": color, "gender": gender},
        {"category": category, "gender": gender},
        {"category": category},
        {}
    ]

    for f in priority_filters:
        filtered = {k: v for k, v in f.items() if v}
        pipeline = [
            {
                "$vectorSearch": {
                    "queryVector": vector,
                    "path": "vector",
                    "numCandidates": 100,
                    "limit": limit,
                    "index": "vector_index",
                    "filter": filtered
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
        ]

        results = list(get_collection().aggregate(pipeline))
        if results:
            print(f"✅ Found {len(results)} with filter: {filtered}")
            return results

    print("❌ No matches found with any filter.")
    return []
