// frontend/src/App.js
import { useState } from "react";
import axios from "axios";
import './App.css';

function App() {
  const [image, setImage] = useState(null);
  const [visionAdvice, setVisionAdvice] = useState("");
  const [recommendations, setRecommendations] = useState([]);

  const API = process.env.REACT_APP_API_BASE || "http://127.0.0.1:8000";

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleGeminiVision = async () => {
    const formData = new FormData();
    formData.append("file", image);

    try {
      const res = await axios.post(`${API}/vision/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setVisionAdvice(res.data.response.full_advice);
      setRecommendations(res.data.response.results || []);
    } catch (err) {
      console.error("❌ Gemini Vision failed to generate a response.", err);
      setRecommendations([]);
    }
  };

  return (
    <div className="App">
      <h1>🧠 AI Stylist</h1>
      <div style={{ display: "flex", gap: "2rem", padding: "2rem" }}>
        {/* Left Column */}
        <div style={{ flex: "1", maxWidth: "300px" }}>
          <h2>🎯 Upload & Search</h2>

          {/* upload image */}
          <input type="file" accept="image/*" onChange={handleImageChange} />
          {image && (
            <div style={{ margin: "1rem" }}>
              <img
                src={URL.createObjectURL(image)}
                alt="Preview"
                width="100%"
                style={{ borderRadius: "8px" }}
              />
            </div>
          )}

          <button onClick={handleGeminiVision}>Try Gemini Vision</button>
        </div>

        {/* Right Column */}
        <div style={{ flex: "2" }}>
          {visionAdvice && (
            <>
              <h3>🧠 Gemini Vision Result:</h3>
              <p>{visionAdvice}</p>

              {recommendations.map((block, i) => (
                <div
                  key={i}
                  style={{
                    marginTop: "2rem",
                    padding: "1rem",
                    background: "#f9f9f9",
                    borderRadius: "8px",
                    border: "1px solid #ddd"
                  }}
                >
                  <h4>🎯 Recommendation #{i + 1}</h4>
                  <p><strong>Title:</strong> {block.item.title}</p>
                  <p><strong>Category:</strong> {block.item.category}</p>
                  <p><strong>Color:</strong> {block.item.color}</p>
                  <p><strong>Gender:</strong> {block.item.gender}</p>
                  <p><strong>Style Tags:</strong> {block.item.style_tags.join(", ")}</p>

                  {block.similar_items?.length > 0 ? (
                    <>
                      <h5>🧩 Similar Items</h5>
                      <div className="results">
                        {block.similar_items.map((item, j) => (
                          <div key={j} className="card">
                            <img src={item.image_url} alt={item.title} width="120" />
                            <p><strong>{item.title}</strong></p>
                            <p>{item.style_tags?.join(", ")}</p>
                            <p><em>Score: {item.score?.toFixed(2)}</em></p>
                          </div>
                        ))}
                      </div>
                    </>
                  ) : (
                    <p>No similar items found.</p>
                  )}
                </div>
              ))}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
