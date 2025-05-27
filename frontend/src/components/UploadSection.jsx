import { useRef } from 'react';
import RemoveImageButton from './RemoveImageButton';
import PreviewImage from './PreviewImage';
import { CloudArrowUpIcon } from '@heroicons/react/24/outline';
import ButtonWrapper from './SpotlightButton';

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
      <div className="flex flex-col items-center">
        <h2 className="flex items-center justify-center text-lg font-semibold gap-2">
          <CloudArrowUpIcon className="w-5 h-5 text-indigo-600" />
          Upload & Search
        </h2>
        <div className="flex justify-center gap-4 mt-2">
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            ref={fileInputRef}
            className="block"
          />
          <RemoveImageButton visible={!!image} onClick={handleRemoveImage} />
        </div>
      </div>

      <PreviewImage image={image} />

      <ButtonWrapper onClick={onAnalyze}>
        ✨ Style This Look
      </ButtonWrapper>
    </div>
  );
}