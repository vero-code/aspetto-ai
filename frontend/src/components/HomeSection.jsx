import { useState } from 'react';
import axios from "axios";
import UploadSection from './UploadSection.jsx';
import { BoltIcon } from '@heroicons/react/24/outline'

export default function HomeSection() {
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
    <div>
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl lg:text-center">
          <h2 className="text-base/7 font-semibold text-indigo-600">Aspetto AI</h2>
          <p className="mt-2 text-4xl font-semibold tracking-tight text-pretty text-gray-900 sm:text-5xl lg:text-balance">
            Everything you need to upgrade your style
          </p>
          <p className="mt-6 text-lg/8 text-gray-600">
            Upload your item, and Gemini AI, along with the latest MongoDB vector search, will select exactly what suits you from a collection of 44,000 products.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-20 gap-y-12 mt-12">
          <UploadSection
            image={image}
            setImage={setImage}
            onAnalyze={handleGeminiVision}
          />
          <div className="flex items-start gap-2 text-gray-600">
            <BoltIcon className="w-5 h-5 mt-1 text-indigo-500" />
            <p className="read-the-docs">
              To see the tip, upload a photo and click the "Style This Look" button
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
