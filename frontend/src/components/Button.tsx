import React from 'react'

const Button = props => {
  return (
    <button
        onClick={props.onClick}
        className="bg-red-500 text-white p-1 rounded hover:bg-red-400"
        >
        {props.text}
    </button>
  )
}



export default Button