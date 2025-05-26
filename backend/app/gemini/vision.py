# backend/app/gemini/vision.py

import google.generativeai as genai
from dotenv import load_dotenv
import os
import io
from PIL import Image
import re
from app.services.generate_vector import generate_vector_from_title
from app.services.vector_search import search_similar_items

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

def generate_vision_advice_from_bytes(image_bytes, prompt: str = None):
    """Generates styling advice + one structured fashion item (name, description, tags) from an image."""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")

        gemini_model = genai.GenerativeModel(MODEL_ID)

        prompt = (
            "You are a fashion stylist. Analyze the uploaded clothing item and give a few style suggestions — "
            "what to wear it with and how.\n\n"
            "After the advice, choose ONE SINGLE fashion item (from the suggestions) to highlight.\n"
            "🛑 IMPORTANT:\n"
            "- The item must be a standalone fashion item (e.g., 'shirt', 'skirt', 'bag', 'shoes').\n"
            "- Do NOT include full outfits or multiple items.\n"
            "- Then, output exactly this structure, on new lines:\n\n"
            "Name: ...\n"
            "Description: ...\n"
            "Tags: ... (comma-separated keywords)"
        )

        response = gemini_model.generate_content(
            [prompt, image],
            generation_config={
                "temperature": 1.0,
                "top_p": 0.95,
                "max_output_tokens": 8192
            }
        )

        full_text = response.text
        parsed = parse_structured_item(full_text)

        if parsed:
            vector = generate_vector_from_title(parsed["title"])
            similar = search_similar_items(vector)
        else:
            vector = []
            similar = []

        return {
            "full_advice": full_text,
            "parsed_item": parsed,
            "vector": vector,
            "similar_items": similar
        }

    except Exception as e:
        print(f"❌ Error in Gemini Vision processing: {e}")
        return {"error": str(e)}

def parse_structured_item(response_text: str):
    """Extracts the Name, Description, and Tags block from Gemini output."""
    match = re.search(r"Name:\s*.+?Tags:\s*.+", response_text, re.DOTALL | re.IGNORECASE)
    if match:
        structured_block = match.group(0)
        pattern = r"Name:\s*(.+?)\s*Description:\s*(.+?)\s*Tags:\s*(.+)"
        inner = re.search(pattern, structured_block, re.DOTALL | re.IGNORECASE)
        if inner:
            title = inner.group(1).strip()
            description = inner.group(2).strip()
            tags = [tag.strip() for tag in inner.group(3).split(",") if tag.strip()]
            return {
                "title": title,
                "description": description,
                "tags": tags
            }
    else:
        return None