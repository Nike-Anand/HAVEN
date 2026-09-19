import axios from "axios";

/**
 * HAVEN API client.
 *
 * DEV: the Vite proxy (see vite.config.js) forwards /auth /sos /therapy /legal
 *      /contacts to the LOCAL FastAPI backend at http://127.0.0.1:8000, so the
 *      app runs fully offline with zero AWS cost while you develop.
 * PROD: a production build (import.meta.env.DEV === false) points at the live
 *      AWS API Gateway by default.
 * OVERRIDE: set VITE_API_URL (in your .env) to force a specific base URL.
 */
const DEFAULT_PROD_URL =
  "https://6qc8x2kc9i.execute-api.eu-north-1.amazonaws.com/dev";
const API_BASE_URL =
  import.meta.env.VITE_API_URL || (import.meta.env.DEV ? "/" : DEFAULT_PROD_URL);
const client = axios.create({ baseURL: API_BASE_URL, timeout: 20000 });

// Attach the Bearer token to every request when present.
client.interceptors.request.use((config) => {
  const token = localStorage.getItem("haven_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// On 401, clear the session and redirect to login.
client.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem("haven_token");
      localStorage.removeItem("haven_user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  },
);

export function apiError(error) {
  return error?.response?.data?.detail || error?.response?.data?.message || "Something went wrong.";
}

export default client;