
export interface ImageData {
    id: string;
    url: string;
    productDisplayName: string;
    gender: string;
    baseColour: string;
    masterCategory: string;
    subCategory: string;
    articleType: string;
    season: string;
    usage: string;
  }

export interface ImageState {
  viewedImage: string | null;
  imageUrls: string[];
  recommendationPage: number;
  modalData: ModalData;
}


export interface ModalData {
  visible: boolean;
  imageData: ImageData | null;
}
