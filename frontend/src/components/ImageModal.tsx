import React from "react";
import { setModalData, setViewedImage } from "../redux/imageSlice";
import { useAppDispatch, useAppSelector } from "../redux/hooks";
import { ModalData } from "../common/types";

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
      className="fixed inset-0 bg-gray-100 bg-opacity-50 overflow-y-auto h-full w-full"
      id="my-modal"
    >
      <div className="relative top-20 mx-auto p-5 border max-w-lg w-11/12 md:w-2/3 lg:w-1/3 xl:w-1/4 shadow-lg rounded-md bg-gray-50">
        <div className="mt-3 text-center">
          <div>
            <img
              src={modalData.imageData === null ? "" : modalData.imageData.url}
              alt="Viewed"
              className="w-full h-auto object-cover rounded"
            />
            <div className="">
              <p className="text-xl mt-2 text-gray-800">
                {modalData.imageData === null
                  ? ""
                  : modalData.imageData.productDisplayName}
              </p>
              <p className="text-lg mt-2 text-gray-400">
                {modalData.imageData === null
                  ? ""
                  : `${modalData.imageData.masterCategory} | ${modalData.imageData.gender} | ${modalData.imageData.usage}`}
              </p>
            </div>
          </div>
          <div className="mt-2 flex">
            <button
              onClick={closeModal}
              className="px-4 py-2 my-2 bg-indigo-700 text-white text-base font-medium tracking-wide rounded-md w-full shadow-sm hover:bg-indigo-600 capitalize transition-colors duration-300 transform"
            >
              Close
            </button>
            <button
              onClick={handleView}
              className="px-4 py-2 m-2 bg-indigo-700 text-white text-base  font-medium tracking-wide rounded-md w-full shadow-sm hover:bg-indigo-600 capitalize transition-colors duration-300 transform"
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
