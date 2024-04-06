import React from "react";
import { setModalData, setViewedImage } from "../redux/imageSlice";
import { useAppDispatch, useAppSelector } from "../redux/hooks";


const ImageModal: React.FC = () => {
  const dispatch = useAppDispatch();
  const modalData = useAppSelector((state) => state.image.modalData);
  // console.log(modalData);
  if (!modalData.visible) {
    return null;
  }

  const closeModal = () => {
    dispatch(setModalData({ visible: false, imageUrl: "", imageId: ""}));
  };
  const handleView = async () => {
    dispatch(
      setViewedImage({
        imageUrl: modalData.imageUrl,
        imageId: modalData.imageId,

      })
    );
    closeModal();
  };
  return (
    <div
      className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full"
      id="my-modal"
    >
      <div className="relative top-20 mx-auto p-5 border max-w-lg w-11/12 md:w-2/3 lg:w-1/3 xl:w-1/4 shadow-lg rounded-md bg-white">
        <div className="mt-3 text-center">
          <img
            src={modalData.imageUrl===null?"":modalData.imageUrl}
            alt="Viewed"
            className="w-full h-auto object-cover rounded"
          />
          <div className="mt-2">
            <button
              onClick={handleView}
              className="px-4 py-2 my-2 bg-indigo-600 text-white text-base  font-medium tracking-wide rounded-md w-full shadow-sm hover:bg-indigo-500 capitalize transition-colors duration-300 transform"
            >
              View
            </button>
            <button
              onClick={closeModal}
              className="px-4 py-2 my-2 bg-indigo-600 text-white text-base font-medium tracking-wide rounded-md w-full shadow-sm hover:bg-indigo-500 capitalize transition-colors duration-300 transform"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImageModal;
