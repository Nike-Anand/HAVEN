import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import client from "../../api/client.js";

function readSession() {
  try {
    const raw = localStorage.getItem("haven_user");
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export const loginUser = createAsyncThunk(
  "auth/login",
  async (credentials) => {
    const { data } = await client.post("/auth/login", credentials);
    return data;
  },
);

export const signupUser = createAsyncThunk(
  "auth/signup",
  async (payload) => {
    const { data } = await client.post("/auth/signup", payload);
    return data;
  },
);

export const fetchProfile = createAsyncThunk(
  "auth/profile",
  async () => {
    const { data } = await client.get("/auth/profile");
    return data;
  },
);

const authSlice = createSlice({
  name: "auth",
  initialState: {
    token: localStorage.getItem("haven_token") || null,
    user: readSession(),
    status: "idle", // idle | loading | ok | error
    error: null,
  },
  reducers: {
    logout(state) {
      state.token = null;
      state.user = null;
      localStorage.removeItem("haven_token");
      localStorage.removeItem("haven_user");
    },
    setToken(state, action) {
      state.token = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginUser.fulfilled, (state, action) => {
        state.token = action.payload.token;
        state.status = "ok";
        localStorage.setItem("haven_token", action.payload.token);
      })
      .addCase(signupUser.fulfilled, (state, action) => {
        state.token = action.payload.token;
        state.status = "ok";
        localStorage.setItem("haven_token", action.payload.token);
      })
      .addCase(fetchProfile.fulfilled, (state, action) => {
        state.user = action.payload;
        localStorage.setItem("haven_user", JSON.stringify(action.payload));
      })
      .addCase(fetchProfile.rejected, (state) => {
        state.status = "error";
      });
  },
});

export const { logout, setToken } = authSlice.actions;
export default authSlice.reducer;