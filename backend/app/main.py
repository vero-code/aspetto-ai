from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .vision_ai import analyze_image_bytes
from .mongodb import collection

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

@app.post("/analyze/")
async def analyze_image(file: UploadFile = File(...)):
    print("📥 File received:", file.filename)

    image_bytes = await file.read()
    print("🧠 Passing an image to the Vision API...")

    tags = analyze_image_bytes(image_bytes)
    print("🏷️ Tags from Vision API:", tags)

    doc = {
        "image_filename": file.filename,
        "tags": tags,
        "vector": None,
        "source": "user"
    }

    print("💾 Save the result in MongoDB...")
    collection.insert_one(doc)

    print("✅ Everything is ready. Return the result.")
    return {"tags": tags}