interface ButtonProps {
  onClick: () => void;
  text: string;
}

const Button = (props:ButtonProps) => {
  return (
    <button
        onClick={props.onClick}
        className="flex items-center px-1 py-1 mr-2 font-medium tracking-wide text-white capitalize transition-colors duration-300 transform bg-indigo-700 rounded-lg hover:bg-indigo-600"
        >
        {props.text}
    </button>
  )
}



export default Button