import { useState } from 'react'
import axios from "axios";
import './App.css';
import UploadSection from './components/UploadSection.jsx';

function App() {
  const [image, setImage] = useState(null);
  const [visionAdvice, setVisionAdvice] = useState("");
  const [recommendations, setRecommendations] = useState([]);

  const API = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

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
    <main className="max-w-6xl mx-auto px-4 pt-12">
      <h1 className="text-3xl font-bold text-center">Aspetto AI</h1>
      <div className="text-center text-red-500 text-2xl mt-2">Your style assistant</div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-x-20 gap-y-12 mt-12">
        <UploadSection
          image={image}
          setImage={setImage}
          onAnalyze={handleGeminiVision}
        />
        <div>
          <p className='read-the-docs'>To see the tip, upload a photo and click the "Style This Look" button</p>
        </div>
      </div>
    </main>
  )
}

export default App;