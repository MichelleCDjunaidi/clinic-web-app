import axios from 'axios'
import router from '../router'

// Set base URL - works both in Docker and local development
axios.defaults.baseURL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000' 
  : 'http://backend:8000'

// Request interceptor to add JWT token
axios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle 401 errors
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('doctor')
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

export default axios