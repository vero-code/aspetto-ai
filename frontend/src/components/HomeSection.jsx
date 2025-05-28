import { useState } from 'react';
import axios from "axios";
import UploadSection from './UploadSection.jsx';
import { BoltIcon } from '@heroicons/react/24/outline';
import HomeSectionHeader from './HomeSectionHeader.jsx';
import SpringModal from './SpringModal.jsx';
import ReactMarkdown from 'react-markdown';
import RecommendationsGrid from './RecommendationsGrid.jsx';

export default function HomeSection() {
  const [image, setImage] = useState(null);
  const [visionAdvice, setVisionAdvice] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const API = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

  const handleGeminiVision = async () => {
    if (!image) {
      setIsModalOpen(true);
      return;
    }

    setIsLoading(true);
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
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <div className="w-full px-6 lg:px-8">
        <HomeSectionHeader />
        <div className="grid grid-cols-1 md:grid-cols-[0.5fr_2.5fr] gap-x-5 gap-y-12 mt-12">
          <UploadSection
            image={image}
            setImage={setImage}
            onAnalyze={handleGeminiVision}
            clearResults={() => {
              setVisionAdvice("");
              setRecommendations([]);
            }}
          />
          <div className="flex items-start gap-2 text-gray-600">
            {isLoading && !visionAdvice && (
              <div className="flex justify-center items-center w-full h-32">
                <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-500" />
              </div>
            )}

            {!visionAdvice && !isLoading && (
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
                  <div>
                    <h2 className="text-xl font-semibold mb-2">
                      🧠 Your recommendations from AI stylist:
                    </h2>
                    <div className="mt-4 rounded-xl overflow-hidden bg-white shadow-md ring-1 ring-slate-200 p-6 max-w-7xl mx-auto">
                      <div className="text-lg leading-relaxed mb-6 text-left">
                        <ReactMarkdown>{visionAdvice}</ReactMarkdown>
                      </div>
                    </div>
                  </div>

                  <RecommendationsGrid recommendations={recommendations} />
                </>
              )}
            </div>
          </div>
        </div>
      </div>
      <SpringModal isOpen={isModalOpen} setIsOpen={setIsModalOpen} />
    </div>
  )
}
