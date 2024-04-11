import axios from "axios";

export default axios.create({baseURL: import.meta.env.VITE_REACT_APP_BACKEND_URL,headers: {'Content-type': 'application/json',"Access-Control-Allow-Origin":"*"}});