// frontend/src/App.js
import { useState } from "react";
import axios from "axios";
import './App.css';

function App() {
  const [image, setImage] = useState(null);
  const [visionAdvice, setVisionAdvice] = useState("");
  const [visionItem, setVisionItem] = useState(null);
  const [similarToGemini, setSimilarToGemini] = useState([]);

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
      setVisionItem(res.data.response.parsed_item);
      setSimilarToGemini(res.data.response.similar_items || []);
    } catch (err) {
      console.error("❌ Gemini Vision failed to generate a response.", err);
      setVisionItem(null);
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

          {/* vision/ */}
          <button onClick={handleGeminiVision}>Try Gemini Vision</button>
        </div>

        {/* Right Column */}
        <div style={{ flex: "2" }}>
          {/* vision/ */}
          {visionAdvice && (
            <>
              <h3>🧠 Gemini Vision Result:</h3>
              <p>{visionAdvice}</p>

              {visionItem && (
                <div style={{ marginTop: "1rem", padding: "1rem", background: "#f3f3f3", borderRadius: "8px" }}>
                  <h4>🎯 Highlighted Recommendation</h4>
                  <p><strong>Title:</strong> {visionItem.title}</p>
                  <p><strong>Category:</strong> {visionItem.category}</p>
                  <p><strong>Color:</strong> {visionItem.color}</p>
                  <p><strong>Gender:</strong> {visionItem.gender}</p>
                  <p><strong>Style Tags:</strong> {visionItem.style_tags?.join(", ") || "—"}</p>
                </div>
              )}

              {similarToGemini.length > 0 && (
                <>
                  <h4>🧩 Similar Items from Collection</h4>
                  <div className="results">
                    {similarToGemini.map((item, i) => (
                      <div key={i} className="card">
                        <img src={item.image_url} alt={item.title} width="120" />
                        <p><strong>{item.title}</strong></p>
                        <p>{item.style_tags?.join(", ")}</p>
                        <p><em>Score: {item.score?.toFixed(2)}</em></p>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
