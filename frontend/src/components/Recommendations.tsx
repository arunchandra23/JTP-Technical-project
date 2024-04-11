import React, { useEffect } from "react";
import request from "../request";
import { fetchRandomProducts } from "../utils";
import { useAppDispatch, useAppSelector } from "../redux/hooks";
import { setImageUrls, setModalData } from "../redux/imageSlice";
import { ImageData } from "../common/types";
import ImageCard from "./ImageCard";


interface RecommendationsProps {
  handleRefresh: () => void;
}
const Recommendations: React.FC<RecommendationsProps> = ({ handleRefresh }) => {
  const imageUrls: ImageData[] = useAppSelector(
    (state) => state.image.imageUrls
  );
  const recommendationPage = useAppSelector(
    (state) => state.image.recommendationPage
  );
  const viewedImage: any = useAppSelector((state) => state.image.viewedImage);

  const dispatch = useAppDispatch();

  useEffect(() => {
    fetchRandomProducts(dispatch);
  }, [viewedImage]);
  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const response = await request.get(
          `/get-recommendations/?image_id=${
            viewedImage.imageId
          }&collection_name=${
            import.meta.env.VITE_REACT_APP_QDRANT_COLLECTION
          }&top_k=10&page=${recommendationPage}`
        );
        dispatch(setImageUrls(response.data)); // Assuming the API returns an array of image URLs
      } catch (error) {
        console.error("Failed to fetch images", error);
      }
    };
    if (viewedImage !== null) fetchRecommendations();
  }, [viewedImage, recommendationPage]);
  const handleView = async (image:ImageData) => {
    dispatch(setModalData({ visible: true, imageData:image}));
  };

  return (
    <>
      <div className="w-full flex  justify-between items-center">
        <h1 className="text-3xl">Recommendations</h1>
        <div className="">
          <button
            onClick={handleRefresh}
            className="flex items-center px-1 py-1 mr-2 font-medium tracking-wide text-white capitalize transition-colors duration-300 transform bg-indigo-700 rounded-lg hover:bg-indigo-600"
          >
            <svg
              className="w-5 h-5 mx-1"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
                clipRule="evenodd"
              />
            </svg>

            <span className="mx-1">Refresh</span>
          </button>
        </div>
      </div>
      <div className="bg-gray-200 w-auto h-0.5"></div>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 max-h-96 overflow-y-scroll px-4 py-8 bg-gray-100">
        {imageUrls.map((image, index) => (
          <ImageCard key={index} image={image} onClick={handleView} />
        ))}
      </div>
    </>
  );
};

export default Recommendations;
