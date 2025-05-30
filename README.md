# 👗 Aspetto AI – Personal Fashion Recommender

[![Cloud Run](https://img.shields.io/badge/Cloud%20Run-deployed-blue.svg)](https://ai-in-action-459717.web.app) [![Made with FastAPI](https://img.shields.io/badge/backend-FastAPI-green.svg)](https://fastapi.tiangolo.com/) [![Frontend: Firebase Hosting](https://img.shields.io/badge/frontend-Firebase-orange.svg)](https://firebase.google.com/) [![MongoDB Vector Search](https://img.shields.io/badge/MongoDB-Vector_Search-brightgreen.svg)](https://www.mongodb.com/products/platform/vector-search) [![Built with Gemini](https://img.shields.io/badge/AI-Gemini_1.5_Pro-purple.svg)](https://deepmind.google/technologies/gemini/)

> Analyze outfits, get fashion advice, and explore similar styles — all powered by AI in the cloud.

AI Stylist is a web app that analyzes your outfit photo and gives personalized fashion insights and item recommendations using Google Gemini and MongoDB Vector Search.

## ⚙️ Stack

- **Frontend**: React + Tailwind CSS, deployed via **Firebase Hosting**
- **Backend**: FastAPI (Python), containerized with Docker, deployed on **Cloud Run** using **Cloud Build** and **Artifact Registry**
- **Database**: MongoDB Atlas with **Vector Search**
- **AI**: Gemini Vision + custom prompt engineering
- **Embeddings Generator**: [thenlper/gte-small](https://huggingface.co/thenlper/gte-small) an open-source General Text Embeddings (GTE) model from Hugging Face
- **Dataset**: [Fashion Product Images Dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset/code) (44k products) from Kaggle

## ✨ Features

- Upload a photo of your outfit
- Get vision-based fashion advice from an AI
- Browse semantic recommendations powered by vector search
- Stylish UI with markdown-formatted advice and tag-based item breakdown

## 🧠 How It Works

1. Image is sent to a FastAPI backend
2. Gemini analyzes the image and returns structured fashion advice
3. Advice is vectorized using GTE model
4. Searched in MongoDB to find semantically similar items
5. Results and insights are returned to the frontend

## 🛠️ Local Development

### ⚙️ Configure

Create and fill out `backend/.env` and `frontend/.env` files.
> Example files are provided in the respective folders.

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m venv venv
venv\Scripts\activate
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── gemini/
│   │   └── vision.py                      # Processes image → extracts data
│   ├── services/
│   │   ├── generate_vector.py             # Creates a vector
│   │   └── vector_search.py               # Vector Search in MongoDB
│   └── main.py                            # FastAPI endpoints
│
├── data/                                  # Examples csv files
│
└── scripts/
    ├── db/
    │   ├── connect.py                     # Connecting to MongoDB Atlas
    │   └── crud.py                        # CRUD operations
    │
    ├── prepare/
    │   ├── embedding/
    │   │   ├── build_text.py              # Prepares .csv file for vectorization
    │   │   └── generate_vectors_to_csv.py # Generate embeddings for .csv file
    │   ├── fix_styles_csv.py              # Replaces commas with quotes
    │   └── merge_with_images.py           # Combines metadata with images
    │
    └── upload/
        └── upload_final_dataset.py        # Loads prepared data into MongoDB
...
```

## 📄 License

This project is licensed under the MIT License — see the LICENSE file for details.