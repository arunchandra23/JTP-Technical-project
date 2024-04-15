import React from "react";
import { setModalData, setViewedImage } from "../redux/imageSlice";
import { useAppDispatch, useAppSelector } from "../redux/hooks";
import { ModalData } from "../common/types";

/**
 * Represents a modal component for displaying an image.
 */

const ImageModal: React.FC = () => {
  
  const dispatch = useAppDispatch();
  const modalData: ModalData = useAppSelector((state) => state.image.modalData);
  // console.log(modalData);
  if (!modalData.visible) {
    return null;
  }

  const closeModal = () => {
    dispatch(setModalData({ visible: false, imageUrl: "", imageId: "" }));
  };
  const handleView = async () => {
    dispatch(
      setViewedImage({
        url: modalData.imageData === null ? "" : modalData.imageData.url,
        imageId: modalData.imageData === null ? "" : modalData.imageData.id,
      })
    );
    closeModal();
  };
  return (
    <div
      className="fixed inset-0 flex items-center justify-center bg-gray-100 bg-opacity-50 overflow-y-auto"
      id="my-modal"
    >
      <div className="m-4 p-5 border max-w-lg w-full sm:w-5/6 md:w-2/3 lg:w-1/2 xl:w-1/3 shadow-lg rounded-md bg-gray-50">
        <div className="text-center">
          <div>
            <img
              src={modalData.imageData ? modalData.imageData.url : ""}
              alt="Viewed"
              className="mx-auto w-auto max-h-60 h-auto object-cover rounded"
            />
            <div>
              <p className="text-xl mt-2 text-gray-800">
                {modalData.imageData
                  ? modalData.imageData.productDisplayName
                  : ""}
              </p>
              <p className="text-lg mt-2 text-gray-400">
                {modalData.imageData
                  ? `${modalData.imageData.masterCategory} | ${modalData.imageData.gender} | ${modalData.imageData.usage}`
                  : ""}
              </p>
            </div>
          </div>
          <div className="flex justify-around mt-2">
            <button
              onClick={closeModal}
              className="px-4 py-2 my-2 w-full bg-indigo-700 text-white text-base font-medium tracking-wide rounded-md shadow-sm hover:bg-indigo-600 capitalize transition-colors duration-300 transform"
            >
              Close
            </button>
            <button
              onClick={handleView}
              className="px-4 py-2 m-2 w-full bg-indigo-700 text-white text-base font-medium tracking-wide rounded-md shadow-sm hover:bg-indigo-600 capitalize transition-colors duration-300 transform"
            >
              View
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImageModal;
