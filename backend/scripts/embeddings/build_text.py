# backend/scripts/embeddings/build_text.py

def build_text_from_row(row: dict) -> str:
    """
    Converts a pandas row (from CSV) into a unified string for embedding.
    """
    parts = [
        str(row.get("productDisplayName", "")),
        str(row.get("articleType", "")),
        str(row.get("baseColour", "")),
        str(row.get("gender", "")),
        str(row.get("usage", "")),
        str(row.get("season", ""))
    ]
    return " | ".join(p for p in parts if p)