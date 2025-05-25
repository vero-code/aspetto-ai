// frontend/src/App.js
import { useState } from "react";
import axios from "axios";
import './App.css';

function App() {
  const [image, setImage] = useState(null);
  const [results, setResults] = useState([]);
  const [textQuery, setTextQuery] = useState("");
  const [analyzeTags, setAnalyzeTags] = useState([]);
  const [vectorPreview, setVectorPreview] = useState([]);
  const [visionAdvice, setVisionAdvice] = useState("");
  const [visionItem, setVisionItem] = useState(null);
  const [similarToGemini, setSimilarToGemini] = useState([]);

  const API = process.env.REACT_APP_API_BASE || "http://127.0.0.1:8000";

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleAnalyze = async () => {
    if (!image) return alert("Upload an image first");
    const formData = new FormData();
    formData.append("file", image);

    try {
      const res = await axios.post(`${API}/analyze/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setAnalyzeTags(res.data.tags);
      setVectorPreview(res.data.vector.slice(0, 5));
      setResults([]);
    } catch (err) {
      console.error("Analyze error:", err);
    }
  };

  const handleTextSearch = async () => {
    try {
      const res = await axios.post(`${API}/search/`, { query: textQuery });
      setResults(res.data.results);
    } catch (err) {
      console.error("Text search error:", err);
    }
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

          {/* analyze/ */}
          <button onClick={handleAnalyze} style={{ marginTop: "1rem" }}>Save in collection</button>

          {/* search/ */}
          <div style={{ marginTop: "1.5rem" }}>
            <input
              type="text"
              value={textQuery}
              onChange={(e) => setTextQuery(e.target.value)}
              placeholder="Try: red jacket, modern, winter"
              style={{ width: "100%" }}
            />
            <button onClick={handleTextSearch} style={{ marginTop: "0.5rem" }}>Text Search</button>
          </div>
        </div>

        {/* Right Column */}
        <div style={{ flex: "2" }}>
          {/* analyze/ */}
          {analyzeTags.length > 0 && (
            <>
              <h3>🔬 Image analyzed and saved</h3>
              <ul>{analyzeTags.map((tag, i) => <li key={i}>{tag}</li>)}</ul>
              <p><em>Vector (first 5 dims):</em></p>
              <code>{JSON.stringify(vectorPreview)}</code>
            </>
          )}

          {/* analyze/, search/ */}
          {results.length > 0 && (
            <>
              <h3>🖼️ Similar Items:</h3>
              <div className="results">
                {results.map((item, i) => (
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

          {/* vision/ */}
          {visionAdvice && (
            <>
              <h3>🧠 Gemini Vision Result:</h3>
              <p>{visionAdvice}</p>

              {visionItem && (
                <div style={{ marginTop: "1rem", padding: "1rem", background: "#f3f3f3", borderRadius: "8px" }}>
                  <h4>🎯 Highlighted Recommendation</h4>
                  <p><strong>Name:</strong> {visionItem.title}</p>
                  <p><strong>Description:</strong> {visionItem.description}</p>
                  <p><strong>Tags:</strong> {visionItem.tags.join(", ")}</p>
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
