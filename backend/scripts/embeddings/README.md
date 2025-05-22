# Embeddings Generator with Hugging Face

This script generates semantic embeddings (vectors) for a specified text field in a CSV file using Hugging Face’s [`thenlper/gte-small`](https://huggingface.co/thenlper/gte-small) model.

### 🏃‍♂️ Background

Based on [GenAI-Showcase](https://github.com/mongodb-developer/GenAI-Showcase). Initially, the project used the Cohere Embedding API. However, due to the free-tier limitation, the pipeline was adapted to Hugging Face, an open-source and fully local alternative.

### ✅ Features
- Loads a local CSV dataset
- Generates sentence-level embeddings
- Stores embeddings in a MongoDB collection in the field `vector`
- Ready for use with MongoDB Vector Search index

### 📦 Requirements
- `sentence-transformers`, `pymongo`, `pandas`, `dotenv`, `tqdm`
- `.env` file with `MONGO_URI`

### 🔧 Usage
```bash
python create_embeddings.py \
  --path backend/data/styles_clean.csv \
  --field productDisplayName \
  --db aspetto_db \
  --coll fashion_items
```
> 💡 Tip: If you're running the script from another directory, provide the full path to the CSV file instead.

Resulting MongoDB documents will contain:

```
{
  "productDisplayName": "Turtle Check Men Navy Blue Shirt",
  "vector": [0.123, 0.456, ..., 384 floats]
}
```

The resulting vector will be stored in the vector field for use in MongoDB Vector Search.