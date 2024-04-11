import { setImageUrls } from "./redux/imageSlice";
import request from "./request";

export const fetchRandomProducts = async (dispatch:any) => {
    try {
      const response = await request.get(
        `/get-products/?collection_name=${import.meta.env.VITE_REACT_APP_QDRANT_COLLECTION}&top_k=20`
      );
      dispatch(setImageUrls(response.data)); // Assuming the API returns an array of image URLs
    } catch (error) {
      console.error("Failed to fetch images", error);
    }
  };