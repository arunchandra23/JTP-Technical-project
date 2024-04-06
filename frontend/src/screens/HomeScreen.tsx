import { ImageData } from "../common/types";
import ImageModal from "../components/ImageModal";
import Recommendations from "../components/Recommendations";
import { useAppDispatch, useAppSelector } from "../redux/hooks";
import { setRecommendationPage, setViewedImage } from "../redux/imageSlice";
import { fetchRandomProducts } from "../utils";

const HomeScreen = () => {
  const dispatch = useAppDispatch();
  const viewedImage: ImageData = useAppSelector((state) => state.image.viewedImage);
  const recommendationPage = useAppSelector(
    (state) => state.image.recommendationPage
  );
  const handleRemoveViewedImage = () => {
    dispatch(setViewedImage(null));
    dispatch(setRecommendationPage(0));
  };
  const handleRefresh = () => {
    if (viewedImage !== null) {
      dispatch(setRecommendationPage(recommendationPage + 1));
    } else {
      fetchRandomProducts(dispatch);
    }
  };
  return (
    <div className="flex justify-center items-center  inset-0 py-16 bg-gray-200 overflow-hidden">
      <div className="container mx-auto my-auto p-4 max-w-5xl bg-white rounded-lg shadow-xl">
        <h1 className="text-3xl">Viewed product</h1>
        <div className="bg-gray-600 w-auto h-0.5"></div>
        {viewedImage ? (
          <div className="flex bg-gray-100 rounded-xl border-2 border-gray-400 border-dashed m-2 justify-center items-center p-4">
            <div className="flex justify-center items-center mr-4 rounded-xl border-2 border-gray-700 overflow-hidden">
              <img
                src={viewedImage.url}
                alt="Viewed product"
                className="w-auto h-36"
              />
            </div>
            <div className="w-auto ml-4 flex justify-center items-center ">
              <button
                onClick={handleRemoveViewedImage}
                className="bg-indigo-600 font-medium text-white p-1 rounded hover:bg-indigo-500 capitalize transition-colors duration-300 transform"
              >
                Remove
              </button>
            </div>
          </div>
        ) : (
          <div className="flex items-center justify-center text-center p-4 min-h-44 bg-gray-100 rounded-xl border-2 border-gray-400 border-dashed m-2 ">
            <div>
              <h2 className="text-xl font-semibold">No product viewed yet</h2>
              <p className="text-gray-500">
                Select a product to get recommendations
              </p>
            </div>
          </div>
        )}

        <Recommendations handleRefresh={handleRefresh} />
        <ImageModal />
      </div>
    </div>
  );
};

export default HomeScreen;
