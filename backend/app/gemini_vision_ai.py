import google.generativeai as genai
from dotenv import load_dotenv
import os
import io
from PIL import Image

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: Gemini API key not found in environment variables.")
    exit()

genai.configure(api_key=api_key)

# List available models
# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         print(f'{m.name}: {m.description}')

MODEL_ID = "models/gemini-1.5-pro-latest";

def generate_vision_advice_from_bytes(image_bytes, prompt: str = "Suggest a fashionable outfit that complements this item"):
    """Generates a text response from an image using Gemini Pro Vision."""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")

        model = genai.GenerativeModel(MODEL_ID)
        response = model.generate_content([prompt, image])

        return response.text

    except Exception as e:
        print(f"Error processing request: {e}")
        return None