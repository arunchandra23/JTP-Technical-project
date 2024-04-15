import { PayloadAction, createSlice } from '@reduxjs/toolkit';
import { ModalData, ImageData } from '../common/types';

/**
 * Redux slice for managing image state.
 */
export const imageSlice = createSlice({
  name: 'image',
  initialState: {
    viewedImage: null,
    imageUrls: [],
    recommendationPage: 0,
    modalData: { visible: false, imageData: null },
  },
  reducers: {
    /**
     * Sets the currently viewed image.
     * @param state - The current state.
     * @param action - The payload action containing the image data.
     */
    setViewedImage: (state, action: PayloadAction<ImageData | any>) => {
      state.viewedImage = action.payload;
    },
    /**
     * Sets the image URLs.
     * @param state - The current state.
     * @param action - The payload action containing the array of image URLs.
     */
    setImageUrls: (state, action: PayloadAction<string[] | any>) => {
      state.imageUrls = action.payload;
    },
    /**
     * Removes the currently viewed image.
     * @param state - The current state.
     */
    removeViewedImage: (state) => {
      state.viewedImage = null;
    },
    /**
     * Sets the current recommendation page.
     * @param state - The current state.
     * @param action - The payload action containing the page number.
     */
    setRecommendationPage: (state, action: PayloadAction<number>) => {
      state.recommendationPage = action.payload;
    },
    /**
     * Sets the modal data.
     * @param state - The current state.
     * @param action - The payload action containing the modal data.
     */
    setModalData: (state, action: PayloadAction<ModalData | any>) => {
      state.modalData = action.payload;
    },
  },
});

export const {
  setViewedImage,
  setImageUrls,
  removeViewedImage,
  setRecommendationPage,
  setModalData,
} = imageSlice.actions;

export default imageSlice.reducer;
