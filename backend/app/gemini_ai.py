# gemini_ai.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

def generate_style_advice(item_data: dict) -> str:
    title = item_data.get("title", "")
    tags = ", ".join(item_data.get("style_tags", []))
    color = item_data.get("color", "")
    gender = item_data.get("gender", "")

    prompt = (
        f"Imagine you are a fashion AI stylist.\n"
        f"Cloth: {title}.\n"
        f"Color: {color}, gender: {gender}.\n"
        f"Tags: {tags}.\n"
        f"Please advise what can be added to the image to make it more stylish, "
        f"seasonal or trendy. Keep the tone simple and friendly."
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error generating advice: {e}"