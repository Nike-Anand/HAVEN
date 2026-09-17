import axios from "axios";

/**
 * HAVEN API client.
 *
 * The Vite dev server proxies /auth, /sos, /therapy, /legal, /contacts and
 * /health to the FastAPI backend, so we can use a relative base URL.
 */
const client = axios.create({ baseURL: "/", timeout: 20000 });

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