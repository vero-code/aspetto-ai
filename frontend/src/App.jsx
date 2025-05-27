import { useState } from 'react'
import './App.css'
import SpotlightButton from './components/SpotlightButton.jsx'

function App() {
  const [image, setImage] = useState(null);

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
      console.error("❌ App failed to generate a response.", err);
      setRecommendations([]);
    }
  };

  return (
    <>
      <h1>Aspetto AI Stylist</h1>
      <div className="card">
        <div className="text-red-500 text-2xl">
          Your style assistant
          </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
        <div>
          <h2 className="text-lg font-semibold">🎯 Upload & Search</h2>

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

          <div className="my-6 bg-slate-800 p-4 rounded-lg">
            <SpotlightButton onClick={handleGeminiVision}>
              ✨ Style This Look
            </SpotlightButton>
          </div>
        </div>
        <div>
          <p className='read-the-docs'>To see the tip, upload a photo and click the "Style This Look" button</p>
        </div>
      </div>
    </>
  )
}

export default App;