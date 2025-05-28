export default function RecommendationsGrid({ recommendations }) {
  if (!recommendations || recommendations.length === 0) return null;

  return (
    <div className="w-full flex justify-center">
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-10">
        {recommendations.map((block, i) => (
          <div
            key={i}
            className="bg-white rounded-xl shadow-md p-5 border border-gray-200 hover:shadow-lg transition-all"
          >
            {block.similar_items?.length > 0 && (
              <>
                <div className="space-y-4">
                  {block.similar_items.map((item, j) => (
                    <div
                      key={j}
                      className="max-w-sm rounded overflow-hidden shadow-lg"
                    >
                      <img
                        src={item.image_url}
                        alt={item.title}
                        className="w-full h-200 object-cover mt-4 ml-0 rounded-xl overflow-hidden bg-white shadow-md ring-1 ring-slate-200 transition-transform duration-300 hover:scale-[1.02] hover:shadow-xl cursor-pointer max-w-sm max-h-96 mx-auto"
                      />
                      <div className="px-6 py-4">
                        <h3 className="text-xl font-semibold mb-4 min-h-[3.5rem]">
                          {item.title}
                        </h3>

                        <div class="px-6 pt-4 pb-2">
                          {item.style_tags?.map((tag, i) => (
                            <span 
                              key={i}
                              class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2"
                            >
                              #{tag.toLocaleLowerCase()}
                            </span>
                          ))}
                        </div>
                        <p className="text-gray-400 italic text-sm mt-1">
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
    </div>
  );
}