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
    """Generates styling advice + 3 structured fashion items from an image, each with similar matches."""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")

        gemini_model = genai.GenerativeModel(MODEL_ID)

        prompt = (
            "You are a fashion stylist. Analyze the uploaded clothing item and give a few styling suggestions — "
            "what to wear it with and how.\n\n"
            "Then, based on your suggestions, select and describe exactly THREE standalone complementary fashion items "
            "(e.g., 'shirt', 'skirt', 'bag', 'shoes').\n\n"
            "🛑 IMPORTANT:\n"
            "- Each item must be a SINGLE standalone fashion item (not an outfit or combination).\n"
            "- The items must be diverse and stylistically relevant to the input image.\n"
            "- For each item, output the following structure EXACTLY — one after another:\n\n"
            "Item 1:\n"
            "Title: ...\n"
            "Category: ... (e.g., Shirts, Dresses, Bags — 1 word category)\n"
            "Color: ... (dominant color or best-matching color)\n"
            "Gender: ... (Men or Women)\n"
            "Style Tags: ... (comma-separated keywords)\n\n"
            "Item 2:\n"
            "Title: ...\n"
            "Category: ...\n"
            "Color: ...\n"
            "Gender: ...\n"
            "Style Tags: ...\n\n"
            "Item 3:\n"
            "Title: ...\n"
            "Category: ...\n"
            "Color: ...\n"
            "Gender: ...\n"
            "Style Tags: ..."
        )

        response = gemini_model.generate_content(
            [prompt, image],
            generation_config={
                "temperature": 1.0,
                "top_p": 0.95,
                "max_output_tokens": 8192
            }
        )

        full_response_text = response.text

        cut_index = re.search(r"Item\s*1\s*:", full_response_text, re.IGNORECASE)
        full_advice = (
            full_response_text[:cut_index.start()].strip()
            if cut_index else full_response_text.strip()
        )

        parsed_items = parse_structured_items(full_response_text)

        results = []
        for item in parsed_items:
            vector = generate_vector_from_text_fields(
                title=item["title"],
                category=item.get("category"),
                color=item.get("color"),
                gender=item.get("gender"),
                style_tags=item["style_tags"]
            )
            similar = search_similar_items(
                vector,
                category=item.get("category"),
                color=item.get("color"),
                gender=item.get("gender")
            )
            results.append({
                "item": item,
                "vector": vector,
                "similar_items": similar
            })

        return {
            "full_advice": full_advice,
            "results": results
        }

    except Exception as e:
        print(f"❌ Error in Gemini Vision processing: {e}")
        return {"error": str(e)}

def parse_structured_items(response_text: str) -> list[dict]:
    """Extracts 3 structured fashion item blocks from Gemini output."""
    pattern = (
        r"Item\s*\d+:\s*"
        r"Title:\s*(.+?)\s*"
        r"Category:\s*(.+?)\s*"
        r"Color:\s*(.+?)\s*"
        r"Gender:\s*(.+?)\s*"
        r"Style Tags:\s*(.+?)(?:\n\n|\Z)"
    )

    matches = re.findall(pattern, response_text, re.DOTALL | re.IGNORECASE)

    items = []
    for match in matches:
        item = {
            "title": match[0].strip(),
            "category": match[1].strip(),
            "color": match[2].strip(),
            "gender": match[3].strip(),
            "style_tags": [tag.strip() for tag in match[4].split(",") if tag.strip()]
        }
        items.append(item)

    return items if len(items) == 3 else []