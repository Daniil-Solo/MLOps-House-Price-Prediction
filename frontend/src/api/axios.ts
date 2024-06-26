import axios from "axios";
const MODE = import.meta.env.VITE_MODE;

let apiURL = undefined;
let headers = undefined
if (MODE !== "production"){
    apiURL = import.meta.env.VITE_API_HOST || "";
    headers = {
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
    }
}
const baseAxios = axios.create({
    baseURL: apiURL,
    headers: headers
});


export {baseAxios};