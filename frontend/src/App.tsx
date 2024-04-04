import React, { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import Recommendations from './components/Recommendations';
import Navbar from './components/Navbar';

function App() {
  const [recommendations, setRecommendations] = useState<string[]>([]);

  const handleRecommendations = (images: string[]) => {
    setRecommendations(images);
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Navbar />
      <div className="flex-grow">
        <div className="container mx-auto p-6">
          <div className={`flex flex-row items-center gap-10 ${recommendations.length===0?"justify-center":"justify-between"}`} >
            {/* Upload Section */}
            <div className="w-full max-w-3xl">
              <ImageUpload onRecommendations={handleRecommendations} />
            </div>
            
            {/* Recommendations Section */}
            {recommendations.length > 0 && (
              <div className="w-full max-w-4xl">
                <Recommendations images={recommendations} />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
