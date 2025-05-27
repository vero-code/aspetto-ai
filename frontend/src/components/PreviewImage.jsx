// components/PreviewImage.jsx
export default function PreviewImage({ image }) {
  if (!image) return null;

  return (
      <div className="mt-4 rounded-xl overflow-hidden bg-white shadow-md ring-1 ring-slate-200 transition-transform duration-300 hover:scale-[1.02] hover:shadow-xl cursor-pointer max-w-sm max-h-96 mx-auto">
      <img
        src={URL.createObjectURL(image)}
        alt="Preview"
        className="w-full h-auto object-contain"
      />
    </div>
  );
}