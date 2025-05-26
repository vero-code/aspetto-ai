# backend/app/main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .gemini.vision import generate_vision_advice_from_bytes as generate_vision_advice_from_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Aspetto AI backend is running!"}

@app.post("/vision/")
async def style_from_image(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        result = generate_vision_advice_from_image(image_bytes)

        similar_items = result.get("similar_items", [])
        for item in similar_items:
            item["_id"] = str(item["_id"])

        return {
            "response": {
                "full_advice": result["full_advice"],
                "parsed_item": result["parsed_item"],
                "similar_items": similar_items
            }
        }
    
    except Exception as e:
        print("❌ Error in /vision/:", e)
        return {"error": str(e)}