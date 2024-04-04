// Recommendations.tsx
import React from 'react';

interface Props {
  images: string[];
}

const Recommendations: React.FC<Props> = ({ images }) => {
  return (
    <div className="flex justify-center items-center my-10">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 w-full max-w-8xl mx-auto">
        {images.slice(0, 10).map((image, index) => (
          <div key={index} className="overflow-hidden rounded-lg shadow-lg border-gray-700 border-2">
            <img src={image} alt={`Recommendation ${index + 1}`} className="w-96 h-auto object-cover" />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Recommendations;

