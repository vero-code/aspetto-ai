# backend/app/generate_vector.py
from sentence_transformers import SentenceTransformer
import logging
from functools import lru_cache

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

@lru_cache()
def get_embedding_model():
    logging.info("⚙️ Loading gte-small model from Hugging Face (lazy)...")
    return SentenceTransformer("thenlper/gte-small")

def generate_vector_from_title(title: str) -> list[float]:
    """Returns a vector embedding for a title using gte-small."""
    logging.info(f"🔠 Generating vector for: {title}")
    model = get_embedding_model()
    vector = model.encode([title])[0].tolist()
    logging.info("✅ Vector generated.")
    print("🧬 Vector preview:", vector[:5])
    return vector