# backend/app/gemini/vision.py

import google.generativeai as genai
from dotenv import load_dotenv
import os
import io
from PIL import Image
import re
from app.services.generate_vector import generate_vector_from_text_fields
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
    """Generates styling advice + one structured fashion item from an image."""
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
            "Title: ...\n"
            "Category: ... (e.g., Shirts, Dresses, Bags — 1 word category)\n"
            "Color: ... (dominant color or best-matching color)\n"
            "Gender: ... (Men or Women)\n"
            "Style Tags: ... (comma-separated keywords)"
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
            vector = generate_vector_from_text_fields(
                title=parsed["title"],
                category=parsed.get("category"),
                color=parsed.get("color"),
                gender=parsed.get("gender"),
                style_tags=parsed["style_tags"],
            )
            similar = search_similar_items(
                vector,
                category=parsed.get("category"),
                color=parsed.get("color"),
                gender=parsed.get("gender"),
            )
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
    """Extracts structured item fields from Gemini output."""
    pattern = (
        r"Title:\s*(.+?)\s*"
        r"Category:\s*(.+?)\s*"
        r"Color:\s*(.+?)\s*"
        r"Gender:\s*(.+?)\s*"
        r"Style Tags:\s*(.+)"
    )
    match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
    if match:
        return {
            "title": match.group(1).strip(),
            "category": match.group(2).strip(),
            "color": match.group(3).strip(),
            "gender": match.group(4).strip(),
            "style_tags": [t.strip() for t in match.group(5).split(",") if t.strip()]
        }
    return None