export interface ImageState {
  viewedImage: string | null;
  imageUrls: string[];
  recommendationPage: number;
  modalData: {
    visible: boolean;
    imageUrl: string | null;
    imageId: string | null;
  };
}

export interface ViewedImage {
  imageUrl: string | null;
  imageId: string | null;
}
export interface ModalData {
  visible: boolean;
  imageUrl: string ;
  imageId: string ;
}
