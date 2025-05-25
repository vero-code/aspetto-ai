# backend/app/vision_ai.py
from google.cloud import vision
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from functools import lru_cache
import os

load_dotenv()
key_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
print(f"📁 [vision_ai] Path to the key: {key_path}")

if not key_path or not os.path.exists(key_path):
    raise FileNotFoundError("❌ GOOGLE_APPLICATION_CREDENTIALS not set or file not found in .env.")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

@lru_cache()
def get_vision_client():
    print("⚙️ [vision_ai] Initialize the Vision API client...")
    client = vision.ImageAnnotatorClient()
    print("✅ [vision_ai] Vision API client is ready.")
    return client

@lru_cache()
def get_embedding_model():
    print("⚙️ [vision_ai] Loading embedding model from Hugging Face...")
    model = SentenceTransformer("thenlper/gte-small")
    print("✅ [vision_ai] Model loaded.")
    return model

def analyze_image_bytes(image_bytes: bytes):
    print("📥 [vision_ai] Image bytes received...")
    client = get_vision_client()
    image = vision.Image(content=image_bytes)

    print("📡 [vision_ai] Sending a request to the Vision API...")
    response = client.label_detection(image=image)

    print("📨 [vision_ai] Answer received.")
    labels = response.label_annotations
    tags = [label.description for label in labels]

    print(f"🏷️ [vision_ai] Tags found: {tags}")
    return tags

def generate_vector(tags: list[str]) -> list[float]:
    text = ", ".join(tags)
    print(f"🧠 [vision_ai] Generating vector for: {text}")
    model = get_embedding_model()
    vector = model.encode([text])[0].tolist()
    print(f"✅ [vision_ai] Vector generated.")
    return vector