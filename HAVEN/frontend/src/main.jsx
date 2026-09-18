import { createRoot } from "react-dom/client";
import { createTheme, StyledEngineProvider, ThemeProvider } from "@mui/material/styles";
import { Provider } from "react-redux";
import { BrowserRouter } from "react-router-dom";

import App from "./App.jsx";
import { store } from "./store/store.js";

// HAVEN brand theme (calm navy + safety red), per the SOS-first design.
const theme = createTheme({
  palette: {
    primary: { main: "#1f2d3d", contrastText: "#ffffff" },
    secondary: { main: "#2f3a86" },
    error: { main: "#c62828", light: "#ef5350" },
    background: { default: "#f6f4f0" },
  },
  typography: {
    fontFamily: '"Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
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