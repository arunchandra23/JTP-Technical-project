import request from "./request";
import { setImageUrls } from "./redux/store";

export const fetchRandomProducts = async (dispatch) => {
    try {
      const response = await request.get(
        "/get-products/?collection_name=fashion_t_t_2epochs&top_k=20"
      );
      dispatch(setImageUrls(response.data)); // Assuming the API returns an array of image URLs
    } catch (error) {
      console.error("Failed to fetch images", error);
    }
  };