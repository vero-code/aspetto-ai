## 🏁 Current Progress

- ✅ 📂 Uploaded cleaned CSV data into MongoDB
- ✅ 🤖 Integrated Google Cloud Vision API (image → semantic tags)
- ✅ 🧠 Saved user-uploaded photos with tags in MongoDB
- ✅ 🧬 Implemented embedding generation using Hugging Face (`gte-small`)
- ✅ 🧮 Stored vectors in MongoDB (`vector` field) for Vector Search
- ✅ 🔍 Enabled semantic search using MongoDB Atlas Vector Index

  - Created vector index on `vector` field (384 dimensions, cosine similarity)
  - Added `/search` endpoint to FastAPI
  - User can query with natural language (e.g. `"elegant red dress"`) to retrieve similar fashion items
  - Results sorted by semantic `score`

✅ 🧠 Integrated **Gemini API (Vertex AI)** for personalized style suggestions

- Added `/suggest` endpoint that generates style advice based on clothing metadata (title, tags, color, gender)

- Uses Gemini Pro to provide friendly, trend-aware recommendations in natural language

- Output examples include layering tips, accessories, seasonal matching, and color theory

⏭️  (Next) Build simple React frontend to upload images and display recommendations