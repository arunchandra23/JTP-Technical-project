import React, { useEffect } from "react";
import request from "../request";
import { setImageUrls, setModalData } from "../redux/store";
import { useSelector, useDispatch } from "react-redux";
import { fetchRandomProducts } from "../utils";
interface ImageUrl {
  url: string;
  id: string;
}

const HomeScreen: React.FC = () => {
  const imageUrls: ImageUrl[] = useSelector((state) => state.image.imageUrls);
  const recommendationPage: ImageUrl[] = useSelector(
    (state) => state.image.recommendationPage
  );
  const viewedImage = useSelector((state) => state.image.viewedImage);

  const dispatch = useDispatch();

  useEffect(() => {
    fetchRandomProducts(dispatch);
  }, [viewedImage]);
  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const response = await request.get(
          `/get-recommendations/?image_id=${viewedImage.imageId}&collection_name=fashion_t_t_2epochs&top_k=20&page=${recommendationPage}`
        );
        dispatch(setImageUrls(response.data)); // Assuming the API returns an array of image URLs
      } catch (error) {
        console.error("Failed to fetch images", error);
      }
    };
    if (viewedImage !== null) fetchRecommendations();
  }, [viewedImage, recommendationPage]);
  const handleView = async (imageUrl: string, imageId: string) => {
    dispatch(setModalData({ visible: true, imageUrl, imageId }));
  };

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 max-h-96 overflow-y-scroll px-4 py-8 bg-gray-100">
      {imageUrls.map((image, index) => (
        <div
          key={image.id}
          className="relative flex justify-center items-center rounded-xl border-2 border-gray-700 overflow-hidden bg-white cursor-pointer opacity-100 hover:opacity-80"
          onClick={() => handleView(image.url, image.id)}
        >
          <img src={image.url} alt={`Image ${index}`} className="w-auto h-44" />
        </div>
      ))}
    </div>
  );
};

export default HomeScreen;
