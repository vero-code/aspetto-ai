# backend/scripts/embeddings/build_text.py

def build_text_for_embedding(doc: dict) -> str:
    """
    Assembles a text string from document fields to generate an embedding.
    """
    parts = [
        str(doc.get("title", "")),
        str(doc.get("category", "")),
        str(doc.get("color", "")),
        str(doc.get("gender", "")),
        ", ".join(str(tag) for tag in doc.get("style_tags", []))
    ]

    return " | ".join(part for part in parts if part)