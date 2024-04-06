import { PayloadAction, createSlice } from '@reduxjs/toolkit';
import { ModalData, ViewedImage } from './types';

export const imageSlice = createSlice({
  name: 'image',
  initialState: {
    viewedImage: null,
    imageUrls: [],
    recommendationPage: 0,
    modalData: { visible: false, imageUrl: null, imageId: null },
  },
  reducers: {
    setViewedImage: (state, action: PayloadAction<ViewedImage | any>) => {
      state.viewedImage = action.payload;
    },
    setImageUrls: (state, action: PayloadAction<string[] | any>) => {
      state.imageUrls = action.payload;
    },
    removeViewedImage: (state) => {
      state.viewedImage = null;
    },
    setRecommendationPage: (state, action: PayloadAction<number>) => {
        state.recommendationPage = action.payload;
    },
    // Adjusting the PayloadAction to correctly reflect the expected type
    setModalData: (state, action: PayloadAction<ModalData | any>) => {
        state.modalData = action.payload;
    },
  },
});

export const { setViewedImage, setImageUrls, removeViewedImage,setRecommendationPage,setModalData } = imageSlice.actions;

export default imageSlice.reducer;
