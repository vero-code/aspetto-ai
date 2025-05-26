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

    # Optional filters
    filter_conditions = {}
    if category:
        filter_conditions["category"] = category
    if color:
        filter_conditions["color"] = color
    if gender:
        filter_conditions["gender"] = gender

    # Vector search
    pipeline = [
        {
            "$vectorSearch": {
                "queryVector": vector,
                "path": "vector",
                "numCandidates": 100,
                "limit": limit,
                "index": "vector_index",
                "filter": filter_conditions or {}
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

    results = get_collection().aggregate(pipeline)

    similar_items = list(results)
    print(f"✅ Found {len(similar_items)} similar items.")
    return similar_items
