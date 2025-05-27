import { useRef } from 'react';
import RemoveImageButton from './RemoveImageButton';
import PreviewImage from './PreviewImage';
import SpotlightButton from './SpotlightButton';

export default function UploadSection({ image, setImage, onAnalyze }) {
  const fileInputRef = useRef(null);

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleRemoveImage = () => {
    setImage(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = null;
    }
  };

  return (
    <div>
      <h2 className="text-lg font-semibold">🎯 Upload & Search</h2>

      <div className="flex items-center gap-4 mt-2">
        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          ref={fileInputRef}
          className="block"
        />

        <RemoveImageButton visible={!!image} onClick={handleRemoveImage} />
      </div>

      <PreviewImage image={image} />

      <div className="my-6 bg-slate-800 p-4 rounded-lg">
        <SpotlightButton onClick={onAnalyze}>
          ✨ Style This Look
        </SpotlightButton>
      </div>
    </div>
  );
}