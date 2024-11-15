import axios from 'axios'

// const baseUrl = 'http://127.0.0.1:8000/'
const isDevelopment = import.meta.env.MODE === 'development'
const baseUrl2 = isDevelopment ? import.meta.env.VITE_API_BASE_URL_LOCAL : import.meta.env.VITE_API_BASE_URL_PROD
const AxiosInstance = axios.create({
    baseURL: baseUrl2,
    timeout: 5000, 
    headers:{
        "Content-Type":"application/json",
         accept: "application/json"
    }
})

AxiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('Token')
        if(token){
            config.headers.Authorization = `Token ${token}`
        }
        else{
            config.headers.Authorization = ``
        }
        return config;
    }
)

AxiosInstance.interceptors.response.use(
    (response) => {
        return response
    }, 
    (error) => {
        if(error.response && error.response.status === 401){
            localStorage.removeItem('Token')
            window.location.href ='/'
        }

    }
)

export default AxiosInstance;