# backend/scripts/embeddings/vector_utils.py

import struct
from typing import List
from bson.binary import Binary
from sentence_transformers import SentenceTransformer
from functools import lru_cache

@lru_cache()
def get_model():
    return SentenceTransformer("thenlper/gte-small")

def compress_vector(vector: List[float]) -> Binary:
    """
    Convert a list of float32 into BSON binary format for efficient storage.
    """ 
    float_bytes = struct.pack(f"<{len(vector)}f", *vector)
    return Binary(float_bytes, subtype=0x0A)

def get_embeddings(texts: List[str]) -> List[Binary]:
    """
    Generates text embeddings using the model and returns them as compressed BSON Binary.
    """
    model = get_model()
    vectors = model.encode(texts, show_progress_bar=False)
    return [compress_vector(vec) for vec in vectors]