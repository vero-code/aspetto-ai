from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from .vision_ai import analyze_image_bytes, generate_vector
from .mongodb import collection
from .gemini_ai import generate_style_advice

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

@app.post("/search_image/")
async def search_by_image(file: UploadFile = File(...)):
    print("📷 Image received for search:", file.filename)

    image_bytes = await file.read()
    print("🧠 Analyzing image with Vision API...")

    tags = analyze_image_bytes(image_bytes)
    print("🏷️ Tags extracted:", tags)

    vector = generate_vector(tags)
    print("🔢 Vector created from image")

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": vector,
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
        response.append({
            "image_url": doc.get("image_url"),
            "title": doc.get("title"),
            "style_tags": doc.get("style_tags", []),
            "score": doc.get("score")
        })

    return {"tags": tags, "results": response}

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

@app.post("/suggest/")
async def suggest_advice(request: Request):
    data = await request.json()

    print("🎨 Generating advice for:", data)
    advice = generate_style_advice(data)

    return {"advice": advice}