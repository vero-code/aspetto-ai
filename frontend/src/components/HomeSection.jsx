import { useState } from 'react';
import axios from "axios";
import UploadSection from './UploadSection.jsx';
import { BoltIcon, StarIcon } from '@heroicons/react/24/outline';
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

      setVisionAdvice(formatVisionAdvice(res.data.response.full_advice));
      setRecommendations(res.data.response.results || []);
    } catch (err) {
      console.error("❌ App failed to generate a response.", err);
      setRecommendations([]);
    } finally {
      setIsLoading(false);
    }
  };

  function formatVisionAdvice(rawText) {
    return rawText
      .replace(/(Item\s+\d+:)/gi, '### $1')
      .replace(/(Title:)/gi, '**$1**')
      .replace(/(Category:)/gi, '**$1**')
      .replace(/(Color:)/gi, '**$1**')
      .replace(/(Gender:)/gi, '**$1**')
      .replace(/(Style Tags:)/gi, '**$1**');
  }

  return (
    <div>
      <div className="w-full px-6 lg:px-8">
        <HomeSectionHeader />
        <div className="grid grid-cols-1 md:grid-cols-[0.5fr_2.5fr] gap-x-20 gap-y-12 mt-12">
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
                    <div className="flex items-center gap-2 mb-2">
                      <StarIcon className="w-5 h-5 text-indigo-600" />
                      <h2 className="text-xl font-semibold text-[#213547]">
                        Recommendations from AI stylist:
                      </h2>
                    </div>
                    <div className="mt-7 rounded-xl overflow-hidden bg-white shadow-md ring-1 ring-slate-200 p-6 max-w-7xl mx-auto">
                      <div className="text-lg leading-relaxed mb-6 text-left">
                        <ReactMarkdown
                          components={{
                            p: ({ children }) => (
                              <p className="mb-2 text-gray-800">{children}</p>
                            ),
                          }}
                        >
                          {visionAdvice}
                        </ReactMarkdown>
                        <table className="w-full table-auto mt-10 border border-gray-200 rounded-xl overflow-hidden">
                          <thead className="bg-gray-50 text-base text-left text-gray-700 font-semibold">
                            <tr>
                              <th className="px-4 py-2">Item</th>
                              <th className="px-4 py-2">Title</th>
                              <th className="px-4 py-2">Category</th>
                              <th className="px-4 py-2">Color</th>
                              <th className="px-4 py-2">Gender</th>
                              <th className="px-4 py-2">Style Tags</th>
                            </tr>
                          </thead>
                          <tbody className="text-base text-gray-800">
                            {recommendations.map((block, i) => (
                              <tr key={i} className="border-t">
                                <td className="px-4 py-2 font-medium">Item {i + 1}</td>
                                <td className="px-4 py-2">{block.item.title}</td>
                                <td className="px-4 py-2">{block.item.category}</td>
                                <td className="px-4 py-2">{block.item.color}</td>
                                <td className="px-4 py-2">{block.item.gender}</td>
                                <td className="px-4 py-2">
                                  <div className="flex flex-wrap gap-1">
                                    {block.item.style_tags.map((tag, j) => (
                                      <span key={j} className="bg-gray-200 rounded-full px-2 py-0.5 text-base">
                                        #{tag.toLowerCase()}
                                      </span>
                                    ))}
                                  </div>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
        <RecommendationsGrid recommendations={recommendations} />
      </div>
      <SpringModal isOpen={isModalOpen} setIsOpen={setIsModalOpen} />
    </div>
  )
}
