import { useRef, useState, useCallback } from 'react';
import RemoveImageButton from './RemoveImageButton';
import PreviewImage from './PreviewImage';
import { CloudArrowUpIcon } from '@heroicons/react/24/outline';
import ButtonWrapper from './SpotlightButton';

export default function UploadSection({ image, setImage, onAnalyze, clearResults }) {
  const fileInputRef = useRef(null);
  const [dragOver, setDragOver] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setImage(file);
    }
  };

  const handleRemoveImage = () => {
    setImage(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = null;
    }
    if (clearResults) {
      clearResults();
    }
  };

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setImage(file);
    }
  }, [setImage]);

   const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => {
    setDragOver(false);
  };

  return (
    <div>
      <div className="flex flex-col items-start">
        <div className="flex items-center justify-center gap-2">
          <CloudArrowUpIcon className="w-5 h-5 text-indigo-600" />
          <h2 className="text-xl font-semibold mb-2">
            Upload & Search
          </h2>
        </div>

        {image ? (
          <div className=" flex text-center mt-4 mb-4">
            <p className="text-sm mb-2 pr-30">✅ <strong>{image.name}</strong></p>
            <RemoveImageButton visible={true} onClick={handleRemoveImage} />
          </div>
        ) : (
          <div
            className={`w-full max-w-xs p-6 mt-5 border-2 border-dashed rounded-xl text-center transition ${
              dragOver ? 'border-indigo-600 bg-indigo-50' : 'border-gray-300'
            }`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
          >
            <p className="text-base text-gray-600 mb-3">Drag & drop an image here</p>
            <p className="text-base text-gray-400 mb-3">or</p>
            <label
              htmlFor="file-upload"
              className="text-base text-indigo-600 cursor-pointer hover:underline"
            >
              Choose File
            </label>
            <input
              id="file-upload"
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              ref={fileInputRef}
              className="hidden"
            />
          </div>
        )}
      </div>

      <PreviewImage image={image} />

      <ButtonWrapper onClick={onAnalyze}>
        ✨ Style This Look
      </ButtonWrapper>
    </div>
  );
}