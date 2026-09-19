import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import client from "../../api/client.js";

export const fetchContacts = createAsyncThunk(
  "contacts/fetch",
  async () => {
    const { data } = await client.get("/contacts");
    // Lambda returns a plain array OR { contacts: [...] }
    return Array.isArray(data) ? data : (data.contacts ?? []);
  },
);

export const addContact = createAsyncThunk(
  "contacts/add",
  async (payload) => {
    const { data } = await client.post("/contacts/add", payload);
    return data;
  },
);

export const verifyContact = createAsyncThunk(
  "contacts/verify",
  async ({ contactId, verificationCode }) => {
    const { data } = await client.post(
      `/contacts/${contactId}/verify`,
      { contactId, verification_code: verificationCode },
    );
    return data;
  },
);

export const deleteContact = createAsyncThunk(
  "contacts/delete",
  async (contactId) => {
    const { data } = await client.delete(`/contacts/${contactId}`);
    return data;
  },
);

const contactsSlice = createSlice({
  name: "contacts",
  initialState: {
    list: [],
    status: "idle",
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchContacts.fulfilled, (state, action) => {
        state.list = action.payload;
        state.status = "ok";
      })
      .addCase(addContact.fulfilled, (state, action) => {
        // Append new contact immediately so UI updates without waiting for re-fetch
        if (action.payload?.contact_id) {
          state.list = [...state.list, action.payload];
        }
        state.status = "ok";
      })
      .addCase(deleteContact.fulfilled, (state, action) => {
        // Lambda returns { deleted: contactId } or { contact_id: ... }
        const deleted = action.payload?.deleted || action.payload?.contact_id;
        state.list = state.list.filter((c) => c.contact_id !== deleted);
      });
  },
});

export default contactsSlice.reducer;