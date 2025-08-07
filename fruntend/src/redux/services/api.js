import { createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

export const getMatchingJobs = createAsyncThunk(
  "api/get-matching-jobs",
  async () => {
    const response = await axios.get(
      "http://localhost:8000/api/get-matching-jobs"
    );
    return response.data;
  }
);

export const searchQuery = createAsyncThunk(
  "api/search-query",
  async ({ query }) => {
    const response = await axios.get(
      `http://localhost:8000/api/search-query/${query}`
    );
    return response.data;
  }
);

export const applyJobs = createAsyncThunk("api/apply-jobs", async (jobList) => {
  const response = await axios.post("http://localhost:8000/api/apply", jobList);
  return response.data;
});

export const appliedJobs = createAsyncThunk("api/applied-Jobs", async () => {
  const response = await axios.get("http://localhost:8000/api/applied-jobs/");
  return response.data;
});
