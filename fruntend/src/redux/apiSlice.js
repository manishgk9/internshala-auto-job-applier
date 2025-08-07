import { createSlice } from "@reduxjs/toolkit";
import {
  getMatchingJobs,
  searchQuery,
  appliedJobs,
  applyJobs,
} from "./services/api";
const jobSlice = createSlice({
  name: "jobs",
  initialState: {
    matchingJobs: [],
    searchResults: [],
    appliedJobs: [],
    applyQueue: [],
    applyTask: null,
    status: "idle",
    error: null,
    loading: false,
  },
  reducers: {
    addToQueue: (state, action) => {
      state.applyQueue.push(action.payload);
    },
    removeFromQueue: (state, action) => {
      state.applyQueue = state.applyQueue.filter(
        (job) => job.job_id !== action.payload
      );
    },
    clearQueue: (state) => {
      state.applyQueue = [];
    },
  },
  extraReducers: (builder) => {
    builder
      // getMatchingJobs
      .addCase(getMatchingJobs.pending, (state) => {
        state.status = "loading";
        state.loading = true;
      })
      .addCase(getMatchingJobs.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.matchingJobs = action.payload.response;
        state.loading = false;
      })
      .addCase(getMatchingJobs.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message;
        state.loading = false;
      })

      // searchQuery
      .addCase(searchQuery.pending, (state) => {
        state.status = "loading";
        state.loading = true;
      })
      .addCase(searchQuery.fulfilled, (state, action) => {
        state.searchResults = action.payload.response;
        state.loading = false;
      })
      .addCase(searchQuery.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message;
        state.loading = false;
      })

      // applyJobs
      .addCase(applyJobs.pending, (state) => {
        state.status = "applying";
        state.loading = true;
      })
      .addCase(applyJobs.fulfilled, (state, action) => {
        state.status = "applied";
        state.applyTask = action.payload;
        state.loading = false;
      })
      .addCase(applyJobs.rejected, (state, action) => {
        state.status = "apply_failed";
        state.error = action.error.message;
        state.loading = false;
      })
      // appliedJobs
      .addCase(appliedJobs.pending, (state) => {
        state.loading = true;
      })
      .addCase(appliedJobs.fulfilled, (state, action) => {
        state.appliedJobs = action.payload;
        state.loading = false;
      })
      .addCase(appliedJobs.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message;
        state.loading = false;
      });
  },
});

export const { addToQueue, removeFromQueue, clearQueue } = jobSlice.actions;

export default jobSlice.reducer;
