// ImageUpload.tsx
import React, { useState, useRef } from 'react';

interface Props {
  onRecommendations: (images: string[]) => void;
}

const ImageUpload: React.FC<Props> = ({ onRecommendations }) => {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    if (event.dataTransfer.files && event.dataTransfer.files[0]) {
      setFile(event.dataTransfer.files[0]);
      updatePreview(event.dataTransfer.files[0]);
    }
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
      updatePreview(event.target.files[0]);
    }
  };

  const updatePreview = (file: File) => {
    const fileReader = new FileReader();
    fileReader.onloadend = () => {
      setPreviewUrl(fileReader.result as string);
    };
    fileReader.readAsDataURL(file);
  };

  const handleDelete = () => {
    setFile(null);
    setPreviewUrl(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = ''; // Reset the file input
    }
    onRecommendations([]); // Clear recommendations if you also want to clear previously fetched recommendations
  };


  const handleSubmit = async () => {
    if (file) {
      const formData = new FormData();
      formData.append('file', file); // The API expects the file with the key 'file'

      try {
        // API endpoint as given in the curl command
        const response = await fetch('http://127.0.0.1:8000/find-similar-images/?collection_name=fashion_products_vdb&top_k=10', {
          method: 'POST',
          headers: {
            'accept': 'application/json',
            // 'Content-Type': 'multipart/form-data', // Don't set this when using FormData in browsers
          },
          body: formData,
        });

        if (!response.ok) throw new Error('Network response was not ok.');

        const data = await response.json();
        // Map through the data and extract only the URLs
        const imageUrls = data.map((item: { filename: string; url: string }) => item.url);
        onRecommendations(imageUrls);
      } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        // Handle error state appropriately
      }
    }
  };
  
  return (
    <div className="flex flex-col items-center justify-center min-h-screen"> {/* Full screen height and centered content */}
    <div className="w-full max-w-4xl p-6 bg-gray-100 rounded-xl shadow-lg"> {/* Increased width and padding */}
      {previewUrl ? (
          <div className="relative flex items-center justify-center">
            <img src={previewUrl} alt="Preview" className="h-80 w-auto object-cover rounded-md border-gray-700 border-2" />
            <button
              onClick={handleDelete}
              className="absolute top-0 right-0 bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded-full"
            >
              &times;
            </button>
          </div>
        ) : (
          <div
            onClick={handleClick}
            onDrop={handleDrop}
            onDragOver={(event) => event.preventDefault()}
            className="cursor-pointer p-5 border-2 border-gray-300 border-dashed rounded-lg text-center h-40 flex items-center justify-center"
          >
            Drop or Upload an Image for Similar Recommendations!
            <input ref={fileInputRef} type="file" onChange={handleChange} className="hidden"/>
          </div>
        )}
        <div className="flex items-center justify-center my-5">
        <button onClick={handleSubmit} className="ml-4  self-center bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded">
          Recommend
        </button>

        </div>
      </div>
    </div>
  );
};

export default ImageUpload;
