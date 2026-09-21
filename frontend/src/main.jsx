import { createRoot } from "react-dom/client";
import { CssBaseline, GlobalStyles, createTheme, StyledEngineProvider, ThemeProvider } from "@mui/material";
import { Provider } from "react-redux";
import { BrowserRouter } from "react-router-dom";

import App from "./App.jsx";
import { store } from "./store/store.js";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#ff2e63", light: "#ff6b9d", dark: "#d90443", contrastText: "#ffffff" },
    secondary: { main: "#ffa62b", light: "#ffc76b", dark: "#e68500", contrastText: "#ffffff" },
    success: { main: "#00c292", light: "#61e6c3", dark: "#00a37d", contrastText: "#ffffff" },
    info: { main: "#5aa9ff", light: "#94c9ff", dark: "#1f7ae0", contrastText: "#ffffff" },
    error: { main: "#e53935", light: "#ff6f60" },
    background: { default: "#fff7fb", paper: "#ffffff" },
  },
  shape: { borderRadius: 16 },
  typography: {
    fontFamily: '"Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    h1: { fontWeight: 800 },
    h2: { fontWeight: 800 },
    h3: { fontWeight: 800 },
    h4: { fontWeight: 800 },
    h5: { fontWeight: 700 },
    h6: { fontWeight: 700 },
    button: { textTransform: "none", fontWeight: 700 },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          boxShadow: "none",
          borderRadius: 12,
          "&:hover": { boxShadow: "0 8px 20px rgba(255,46,99,.18)" },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: "0 12px 32px rgba(120,40,90,.08)",
          border: "1px solid rgba(124,58,237,0.08)",
        },
      },
    },
    MuiTextField: {
      defaultProps: { variant: "outlined" },
    },
  },
});

const root = createRoot(document.getElementById("root"));
root.render(
  <StyledEngineProvider injectFirst>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <GlobalStyles
        styles={{
          "*": { boxSizing: "border-box" },
          body: {
            margin: 0,
            background: "linear-gradient(180deg, #fff7fb 0%, #f4f6ff 100%)",
            color: "#1f2937",
          },
          a: { textDecoration: "none" },
          "::-webkit-scrollbar": { width: 10, height: 10 },
          "::-webkit-scrollbar-thumb": { background: "rgba(124,58,237,0.25)", borderRadius: 999 },
        }}
      />
      <Provider store={store}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </Provider>
    </ThemeProvider>
  </StyledEngineProvider>,
);