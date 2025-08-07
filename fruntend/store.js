import { configureStore } from "@reduxjs/toolkit";
import jobsReducer from "./src/redux/apiSlice";
const autoStore = configureStore({
  reducer: {
    jobsStore: jobsReducer,
  },
});

export default autoStore;
