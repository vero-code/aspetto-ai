import React, { useState } from "react";
import axios from "axios";
import './App.css';

function App() {
  const [image, setImage] = useState(null);
  const [tags, setTags] = useState([]);
  const [results, setResults] = useState([]);
  const [advice, setAdvice] = useState("");
  const [textQuery, setTextQuery] = useState("");
  const [analyzeTags, setAnalyzeTags] = useState([]);
  const [vectorPreview, setVectorPreview] = useState([]);

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
      setAdvice("");
    } catch (err) {
      console.error("Analyze error:", err);
    }
  };

  const handleUpload = async () => {
    if (!image) return alert("Upload an image first");
    const formData = new FormData();
    formData.append("file", image);

    try {
      const res = await axios.post(`${API}/search_image/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setTags(res.data.tags);
      setResults(res.data.results);

      const suggestInput = {
        title: res.data.results[0]?.title || "Item",
        style_tags: res.data.results[0]?.style_tags || [],
        color: "Unknown",
        gender: "Unisex",
      };

      const suggestion = await axios.post(`${API}/suggest/`, suggestInput);
      setAdvice(suggestion.data.advice);
    } catch (err) {
      console.error("Upload error:", err);
    }
  };

  const handleTextSearch = async () => {
    try {
      const res = await axios.post(`${API}/search/`, { query: textQuery });
      setResults(res.data.results);
      setAdvice("");
    } catch (err) {
      console.error("Text search error:", err);
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

          {/* analyze/ */}
          <button onClick={handleAnalyze} style={{ marginTop: "1rem" }}>Analyze Only</button>

          {/* search_image */}
          <button onClick={handleUpload} style={{ marginTop: "0.5rem" }}>Upload & Analyze</button>

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

          {tags.length > 0 && (
            <>
              <h3>🏷️ Tags from upload:</h3>
              <ul>{tags.map((tag, i) => <li key={i}>{tag}</li>)}</ul>
            </>
          )}

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

          {advice && (
            <>
              <h3>💡 Style Advice:</h3>
              <p>{advice}</p>
            </>
          )}
        </div>

      </div>
    </div>
  );
}

export default App;
