import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";

import Navbar from "./components/Navbar";
import ImageModal from "./components/ImageModal";
import HomeScreen from "./components/HomeScreen";
import Button from "./components/Button";

import { setViewedImage, setRecommendationPage } from "./redux/store";
import { fetchRandomProducts } from "./utils";

function App() {
  const dispatch = useDispatch();
  const viewedImage = useSelector((state) => state.image.viewedImage);
  const recommendationPage = useSelector(
    (state) => state.image.recommendationPage
  );

  // useEffect(() => {
  //   document.body.style.overflow = "hidden";
  //   return () => {
  //     // Re-enable scrolling when the component unmounts
  //     document.body.style.overflow = "unset";
  //   };
  // }, []);

  const handleRemoveViewedImage = () => dispatch(setViewedImage(null));
  const handleRefresh = () => {
    if (viewedImage !== null) {
      dispatch(setRecommendationPage(recommendationPage + 1));
    } else {
      fetchRandomProducts(dispatch);
    }
  };
  return (
    <>
      <Navbar />
      <div className="flex justify-center items-center fixed inset-0 mt-16 bg-gray-200 overflow-hidden">
        <div className="container mx-auto my-auto p-4 max-w-5xl bg-white rounded-lg shadow-xl">
          {/* <header className="text-2xl font-bold text-center p-4 border-b">
          Image Recommendation System
        </header> */}
          <h1 className="text-3xl">Viewed product</h1>
          <div className="bg-gray-600 w-auto h-0.5"></div>
          {viewedImage ? (
  <div className="flex justify-center items-center flex-col p-4">
    <div className="relative flex justify-center items-center rounded-xl border-2 border-gray-700 overflow-hidden">
      <img src={viewedImage.imageUrl} alt="Viewed product" className="w-44 h-auto"/>
    </div>
      <div className="w-full flex justify-center items-center mt-2">
        <button
          onClick={handleRemoveViewedImage}
          className="bg-red-500 text-white p-1 rounded hover:bg-red-400 transition duration-200 ease-in-out"
        >
          Remove
        </button>
      </div>
  </div>
) : (
  <div className="text-center p-4 min-h-44">
    <h2 className="text-xl font-semibold">No product viewed yet</h2>
    <p className="text-gray-500">
      Select a product to get recommendations
    </p>
  </div>
)}
          <div className="w-full flex justify-between items-center">
            <h1 className="text-3xl">Recommendations</h1>
            <div className="">
              <Button text="Refresh" onClick={handleRefresh} />
            </div>
          </div>
          <div className="bg-gray-600 w-auto h-0.5"></div>
          <div className="max-h-full">
            <HomeScreen />
          </div>
          <ImageModal />
        </div>
      </div>
    </>
  );
}

export default App;
