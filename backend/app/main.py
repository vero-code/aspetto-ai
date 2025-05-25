# backend/app/main.py
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from .vision_ai import analyze_image_bytes, generate_vector
from .mongodb import collection
from .gemini_vision_ai import generate_vision_advice_from_bytes as generate_vision_advice_from_image

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
    """
    Accepts an uploaded image, parses it using the Vision API,
    generates a vector based on the received tags, stores the results in MongoDB
    and returns the tags and vector.
    """
    print("📥 File received:", file.filename)

    image_bytes = await file.read()
    print("🧠 Passing an image to the Vision API...")

    tags = analyze_image_bytes(image_bytes)
    print("🏷️ Tags from Vision API:", tags)

    print("Generating vector from tags")
    vector = generate_vector(tags)

    doc = {
        "image_filename": file.filename,
        "tags": tags,
        "vector": vector,
        "source": "user"
    }

    print("💾 Save the result in MongoDB...")
    collection.insert_one(doc)

    print("✅ Everything is ready. Return the result.")
    return {"tags": tags, "vector": vector}

@app.post("/search/")
async def search_by_text(request: Request):
    data = await request.json()
    query = data.get("query")

    if not query:
        return {"error": "No query provided"}

    print(f"🔍 Search query received: {query}")

    tags = [tag.strip() for tag in query.split(",") if tag.strip()]
    print(f"🧠 Parsed tags: {tags}")

    query_vector = generate_vector(tags)
    print(f"🔢 Vector generated for query")

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": query_vector,
                "path": "vector",
                "numCandidates": 100,
                "limit": 5,
                "index": "vector_index"
            }
        },
        {
            "$project": {
                "image_url": 1,
                "title": 1,
                "style_tags": 1,
                "score": { "$meta": "vectorSearchScore" }
            }
        }
    ])

    response = []
    for doc in results:
        print("📄 RAW result:", doc)
        response.append({
            "image_url": doc.get("image_url", "❌ no image_url"),
            "title": doc.get("title", "❌ no title"),
            "style_tags": doc.get("style_tags", []),
            "score": doc.get("score", "❌ no score")
        })

    return {"results": response}

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