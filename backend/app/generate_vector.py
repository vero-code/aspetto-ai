# backend/app/generate_vector.py
from sentence_transformers import SentenceTransformer
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

_embedding_model = SentenceTransformer("thenlper/gte-small")

def generate_vector_from_title(title: str) -> list[float]:
    """Returns a vector embedding for a title using gte-small."""
    logging.info(f"🔠 Generating vector for: {title}")
    vector = _embedding_model.encode([title])[0].tolist()
    logging.info("✅ Vector generated.")
    print("🧬 Vector preview:", vector[:5])
    return vector