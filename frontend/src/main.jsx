import { createRoot } from "react-dom/client";
import { createTheme, StyledEngineProvider, ThemeProvider } from "@mui/material/styles";
import { Provider } from "react-redux";
import { BrowserRouter } from "react-router-dom";

import App from "./App.jsx";
import { store } from "./store/store.js";

// HAVEN brand theme — bright, friendly, light-only (no dark theme anywhere).
// Primary = vivid magenta/pink, secondary = sunny amber, success = mint green.
const theme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#ff2e63", light: "#ff6b9d", dark: "#d90443", contrastText: "#ffffff" },
    secondary: { main: "#ffa62b", light: "#ffc76b", dark: "#e68500", contrastText: "#ffffff" },
    success: { main: "#00c292", light: "#61e6c3", dark: "#00a37d", contrastText: "#ffffff" },
    info: { main: "#5aa9ff", light: "#94c9ff", dark: "#1f7ae0", contrastText: "#ffffff" },
    error: { main: "#e53935", light: "#ff6f60" },
    background: { default: "#fff6f9", paper: "#ffffff" },
  },
  shape: { borderRadius: 14 },
  typography: {
    fontFamily: '"Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    h4: { fontWeight: 800 },
    h5: { fontWeight: 700 },
    button: { textTransform: "none", fontWeight: 700 },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: { boxShadow: "none", "&:hover": { boxShadow: "0 6px 18px rgba(255,46,99,.25)" } },
      },
    },
    MuiCard: {
      styleOverrides: { root: { boxShadow: "0 8px 30px rgba(120,40,90,.10)" } },
    },
  },
});

const root = createRoot(document.getElementById("root"));
root.render(
  <StyledEngineProvider injectFirst>
    <ThemeProvider theme={theme}>
      <Provider store={store}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </Provider>
    </ThemeProvider>
  </StyledEngineProvider>,
);