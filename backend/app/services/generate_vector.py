# backend/app/services/generate_vector.py

from sentence_transformers import SentenceTransformer
import logging
from functools import lru_cache

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

@lru_cache()
def get_embedding_model():
    logging.info("⚙️ Loading gte-small model from Hugging Face (lazy)...")
    return SentenceTransformer("thenlper/gte-small")

def generate_vector_from_text_fields(title: str, description: str, tags: list[str]) -> list[float]:
    """Generates vector using title + description + tags."""
    text = " | ".join([
        title.strip(),
        description.strip(),
        ", ".join(tags)
    ])
    logging.info(f"🔠 Generating vector for: {title}")
    model = get_embedding_model()
    vector = model.encode([text])[0].tolist()
    logging.info("✅ Vector generated.")
    return vector