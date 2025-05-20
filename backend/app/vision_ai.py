from google.cloud import vision
from dotenv import load_dotenv
import os

load_dotenv()
key_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
print(f"📁 [vision_ai] Path to the key: {key_path}")

if not key_path or not os.path.exists(key_path):
    raise FileNotFoundError("❌ GOOGLE_APPLICATION_CREDENTIALS not set or file not found in .env.")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

print("⚙️ [vision_ai] Initialize the Vision API client...")

try:
    client = vision.ImageAnnotatorClient()
    print("✅ [vision_ai] Vision API client is ready.")
except Exception as e:
    print(f"❌ [vision_ai] Error initializing Vision API: {e}")
    raise e

def analyze_image_bytes(image_bytes: bytes):
    print("📥 [vision_ai] Image bytes received...")
    image = vision.Image(content=image_bytes)

    print("📡 [vision_ai] Sending a request to the Vision API...")
    response = client.label_detection(image=image)

    print("📨 [vision_ai] Answer received.")

    labels = response.label_annotations
    tags = [label.description for label in labels]

    print(f"🏷️ [vision_ai] Tags found: {tags}")
    return tags