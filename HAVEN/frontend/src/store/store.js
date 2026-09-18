import { combineReducers, configureStore } from "@reduxjs/toolkit";

import authSlice from "./slices/authSlice.js";
import contactsSlice from "./slices/contactsSlice.js";
import sosSlice from "./slices/sosSlice.js";

export const store = configureStore({
  reducer: combineReducers({
    auth: authSlice,
    contacts: contactsSlice,
    sos: sosSlice,
  }),
});