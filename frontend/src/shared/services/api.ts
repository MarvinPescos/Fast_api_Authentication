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
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Only redirect to login if we're not already on the login page
      // and if this is not an authentication verification call
      const currentPath = window.location.pathname;
      const isAuthEndpoint =
        error.config?.url?.includes("/auth/me") ||
        error.config?.url?.includes("/auth/login") ||
        error.config?.url?.includes("/auth/register");

      if (currentPath !== "/login" && !isAuthEndpoint) {
        // Clear auth state and redirect
        const { useAuthStore } = await import(
          "../../features/auth/store/authStore"
        );
        useAuthStore.getState().logout();
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;
