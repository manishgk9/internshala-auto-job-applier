import React, { useState } from "react";
import JobCard from "../job_card/JobCard";
import { useSelector, useDispatch } from "react-redux";
import { searchQuery, applyJobs } from "../../redux/services/api";
import { addToQueue } from "../../redux/apiSlice";
import { useNavigate } from "react-router-dom";
import ConfirmModal from "../model_alert/ModelAlert";
const Search = () => {
  const dispatch = useDispatch();
  const store_data = useSelector((state) => state.jobsStore);
  const nevigate = useNavigate();
  const [showConfirm, setShowConfirm] = useState(false);
  // console.log(store_data.searchResults);
  const [query, setQuery] = useState("");
  function onSearch() {
    if (query.length > 3) {
      dispatch(searchQuery({ query }));
      console.log("btn cliked");
    }
  }

  function onApply(job) {
    var job_data = [
      {
        job_id: job.id,
        job_title: job.title,
        company_name: job.company_name,
        url: job.url,
      },
    ];
    dispatch(applyJobs(job_data)).then(() => {
      setShowConfirm(true);
      setTimeout(() => {
        nevigate("/applied");
      }, 2000);
    });
    // nevigate("/applied");
  }
  function onAddQueue(job) {
    var data = {
      job_id: job.id,
      job_title: job.title,
      company_name: job.company_name,
      url: job.url,
      locations: job.locations,
      salary: job.salary,
      experience: job.experience,
    };
    console.log(data);
    const alreadyQueued = (store_data.onAddQueue || []).some(
      (item) => item.job_id === data.job_id
    );
    console.log(alreadyQueued);
    if (!alreadyQueued) {
      dispatch(addToQueue(data));
    }
  }

  return showConfirm ? (
    <ConfirmModal />
  ) : (
    <div className="p-4">
      {/* Search Bar */}
      <div className="flex justify-center mb-6">
        <div className="flex flex-col sm:flex-row gap-2 items-center">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search jobs..."
            className="border px-4 py-2 w-72 rounded"
          />
          <button
            onClick={() => onSearch()}
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          >
            Search
          </button>
        </div>
      </div>
      {store_data.searchResults.length <= 0 ? (
        store_data.loading ? (
          <p className="text-center font-medium text-1xl text-gray-500">
            wait your search loading..
          </p>
        ) : (
          <p className="text-center font-medium text-1xl text-gray-400">
            Search your desigered location or job position
          </p>
        )
      ) : (
        ""
      )}
      {/* Job Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 justify-items-center">
        {store_data.searchResults.map((job) => (
          <JobCard
            key={job.id}
            job={job}
            onApply={onApply}
            onAddQueue={onAddQueue}
          />
        ))}
      </div>
    </div>
  );
};

export default Search;
