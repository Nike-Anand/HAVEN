import axios from "axios";

/**
 * HAVEN API client.
 *
 * DEV (npm run dev): always talks to the LOCAL FastAPI backend through the
 *   Vite proxy (http://127.0.0.1:8000) so localhost work is fully offline,
 *   never hits the paid AWS gateway, and never trips CORS. This is why adding
 *   contacts, therapy & settings all work during development.
 * PROD (vite build): uses VITE_API_URL (see .env) or the live gateway default.
 *
 * IMPORTANT: the VITE_API_URL in `.env` is applied ONLY to production builds.
 * To force a dev override, set VITE_DEV_API_URL instead.
 */
const DEFAULT_PROD_URL =
  "https://6qc8x2kc9i.execute-api.eu-north-1.amazonaws.com/dev";

const API_BASE_URL = import.meta.env.DEV
  ? import.meta.env.VITE_DEV_API_URL || "/"
  : import.meta.env.VITE_API_URL || DEFAULT_PROD_URL;

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