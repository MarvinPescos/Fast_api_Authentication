import axios, { AxiosError } from "axios";
import type { AxiosInstance } from "axios";
import { API_BASE_URL } from "../utils/constant";

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

//request interceptor
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response.data,
  (error: AxiosError) => {
    if (error.response?.status == 401) {
      console.error("Unauthorized, redirecting to login...");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;
