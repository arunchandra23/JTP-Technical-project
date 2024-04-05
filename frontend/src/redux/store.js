import { configureStore, createSlice } from '@reduxjs/toolkit';

export const imageSlice = createSlice({
  name: 'image',
  initialState: {
    viewedImage: null,
    imageUrls: [],
    recommendationPage: 0,
    modalData: {visible: false, imageUrl: null,imageId:null},
  },
  reducers: {
    setViewedImage: (state, action) => {
      state.viewedImage = action.payload;
    },
    setImageUrls: (state, action) => {
      state.imageUrls = action.payload;
    },
    removeViewedImage: (state) => {
      state.viewedImage = null;
    },
    setRecommendationPage: (state, action) => {
        state.recommendationPage = action.payload;
    },
    setModalData: (state, action) => {
        state.modalData = action.payload;
    },
},
});

export const { setViewedImage, setImageUrls, removeViewedImage,setRecommendationPage,setModalData } = imageSlice.actions;

// Configure the store
const store = configureStore({
  reducer: {
    image: imageSlice.reducer,
  },
});

export default store;
