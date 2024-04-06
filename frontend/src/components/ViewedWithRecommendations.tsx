// src/components/ViewedWithRecommendations.tsx
import React from 'react';


interface Props {
  viewedImage: string | null;
  // recommendations: ImageUrl[];
}

const ViewedWithRecommendations: React.FC<Props> = ({ viewedImage }) => (
  <div className="mt-8">
    {viewedImage && (
      <div className="mb-8">
        <h2 className="text-lg font-bold mb-4">Viewed Image</h2>
        <img src={viewedImage} alt="Viewed" className="w-40 max-w-sm h-auto mx-auto" />
      </div>
    )}
  </div>
);

export default ViewedWithRecommendations;
