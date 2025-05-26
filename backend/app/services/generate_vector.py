# backend/app/services/generate_vector.py

from sentence_transformers import SentenceTransformer
import logging
from functools import lru_cache
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

@lru_cache()
def get_embedding_model():
    logging.info("⚙️ Loading gte-small model from Hugging Face (lazy)...")
    return SentenceTransformer("thenlper/gte-small")

def generate_vector_from_text_fields(
    title: str,
    style_tags: list[str],
    category: Optional[str] = None,
    color: Optional[str] = None,
    gender: Optional[str] = None
) -> list[float]:
    """
    Generates vector using title, style tags,
    and optional metadata fields.
    """
    parts = [title.strip()]

    if category:
        parts.append(f"category: {category.strip().lower()}")
    if color:
        parts.append(f"color: {color.strip().lower()}")
    if gender:
        parts.append(f"gender: {gender.strip().lower()}")
    if style_tags:
        parts.append(", ".join([tag.strip().lower() for tag in style_tags]))

    full_text = " | ".join(parts)

    logging.info(f"🔠 Generating vector for: {title}")
    model = get_embedding_model()
    vector = model.encode([full_text])[0].tolist()
    logging.info("✅ Vector generated.")
    return vector