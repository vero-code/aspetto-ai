import { useState } from 'react';
import axios from "axios";
import UploadSection from './UploadSection.jsx';
import { BoltIcon } from '@heroicons/react/24/outline'
import HomeSectionHeader from './HomeSectionHeader.jsx'

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
      <div className="w-full px-6 lg:px-8">
        <HomeSectionHeader />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-20 gap-y-12 mt-12">
          <UploadSection
            image={image}
            setImage={setImage}
            onAnalyze={handleGeminiVision}
          />
          <div className="flex items-start gap-2 text-gray-600">
            {!visionAdvice && (
              <>
                <BoltIcon className="w-5 h-5 mt-1 text-indigo-500" />
                <p className="read-the-docs">
                  To see the tip, upload a photo and click the "Style This Look" button
                </p>
              </>
            )}
            

            <div style={{ flex: "2" }}>
              {visionAdvice && (
                <>
                  <h3 className="text-xl font-semibold mb-2">🧠 Gemini Vision Result:</h3>
                  <p className="text-lg leading-relaxed mb-6">{visionAdvice}</p>

                  <div className="max-h-[300px] overflow-y-auto space-y-6">
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
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
