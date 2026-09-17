import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import client from "../../api/client.js";

export const triggerSOS = createAsyncThunk(
  "sos/trigger",
  async (location) => {
    const { data } = await client.post("/sos/trigger", {
      location,
      severity: "critical",
    });
    return data;
  },
);

export const fetchSOSStatus = createAsyncThunk(
  "sos/status",
  async (sosId) => {
    const { data } = await client.get(`/sos/${sosId}/status`);
    return data;
  },
);

export const cancelSOS = createAsyncThunk(
  "sos/cancel",
  async ({ sosId, reason }) => {
    const { data } = await client.post(`/sos/${sosId}/cancel`, { reason });
    return data;
  },
);

const sosSlice = createSlice({
  name: "sos",
  initialState: {
    active: null, // current active SOS object
    status: "idle",
    error: null,
  },
  reducers: {
    clearActive(state) {
      state.active = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(triggerSOS.fulfilled, (state, action) => {
        state.active = action.payload;
      })
      .addCase(fetchSOSStatus.fulfilled, (state, action) => {
        state.active = action.payload;
      })
      .addCase(cancelSOS.fulfilled, (state) => {
        state.active = null;
      });
  },
});

export const { clearActive } = sosSlice.actions;
export default sosSlice.reducer;