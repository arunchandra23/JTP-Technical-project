import { ImageData } from "../common/types";

interface Props {
  image: ImageData;
  onClick: (image:ImageData) => void;
}
const ImageCard: React.FC<Props> = ({ image, onClick }) => {
  return (
    <div
      key={image.id}
      className=" justify-center items-center rounded-xl shadow-lg p-2 overflow-hidden bg-white cursor-pointer opacity-100 hover:opacity-80"
      onClick={() => onClick(image)}
    >
        
        <div className="flex justify-center items-center">
          <img
            src={image.url}
            alt={`Image ${image.id}`}
            className="w-auto h-44"
          />
        </div>
        <div className="bg-gray-300 w-auto h-0.5 m-2"></div>

        <div className="h-full text-center flex justify-center ">
          <p className="text-sm text-gray-800">
            {image.productDisplayName}
          </p>
        </div>
    </div>
  );
};

export default ImageCard;
