export default function RecommendationsGrid({ recommendations }) {
  if (!recommendations || recommendations.length === 0) return null;

  return (
    <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-10">
      {recommendations.map((block, i) => (
        <div
          key={i}
          className="bg-white rounded-xl shadow-md p-5 border border-gray-200 hover:shadow-lg transition-all"
        >
          <h4 className="text-lg font-semibold text-indigo-600 mb-2">
            🎯 Recommendation #{i + 1}
          </h4>
          <div className="flex justify-between gap-4 text-sm mb-1">
            <p><strong>Title:</strong> {block.item.title}</p>
            <p><strong>Category:</strong> {block.item.category}</p>
          </div>
          <div className="flex justify-between gap-4 text-sm mb-1">
            <p><strong>Color:</strong> {block.item.color}</p>
            <p><strong>Gender:</strong> {block.item.gender}</p>
          </div>
          <p className="text-sm mb-4 text-left">
            <strong>Style Tags:</strong> {block.item.style_tags.join(", ")}
          </p>

          {block.similar_items?.length > 0 && (
            <>
              <h5 className="text-sm font-semibold text-gray-800 mb-3">
                🧩 Similar Items
              </h5>
              <div className="space-y-4">
                {block.similar_items.map((item, j) => (
                  <div
                    key={j}
                    className="flex items-start gap-4 border p-2 rounded-md"
                  >
                    <img
                      src={item.image_url}
                      alt={item.title}
                      className="w-16 h-16 object-contain rounded border"
                    />
                    <div className="text-sm">
                      <p className="font-medium">{item.title}</p>
                      <p className="text-gray-600 text-xs">
                        {item.style_tags?.join(", ")}
                      </p>
                      <p className="text-gray-400 italic text-xs mt-1">
                        Score: {item.score?.toFixed(2)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      ))}
    </div>
  );
}