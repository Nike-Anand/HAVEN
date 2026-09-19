import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Proxy HAVEN API calls to the FastAPI backend during development.
const apiPrefixes = ["/auth", "/sos", "/therapy", "/legal", "/contacts", "/settings", "/sync", "/track", "/health"];

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      ...Object.fromEntries(apiPrefixes.map((p) => [
        p, {
          target: "http://127.0.0.1:8000",
          changeOrigin: true,
        },
      ])),
    },
  },
  build: {
    outDir: "dist",
  },
});