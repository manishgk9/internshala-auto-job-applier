import React from "react";
import { useSelector } from "react-redux";
const JobCard = ({ job, onApply, onAddQueue }) => {
  const isApplied = useSelector(
    (store_data) =>
      store_data?.appliedJobs?.some((j) => j.job_id === job.id) || false
  );
  const isAlreadyQueued = useSelector((state) =>
    state.jobsStore.applyQueue.some((item) => item.job_id === job.id)
  );
  return (
    <div className="w-full max-w-sm bg-white shadow-md rounded-lg overflow-hidden border">
      {/* Company Logo + Title */}
      <div className="p-4">
        <div className="flex items-center space-x-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-800">{job.title}</h3>
            <p className="text-sm text-gray-500">{job.company_name}</p>
          </div>
        </div>

        {/* Info */}
        <div className="mt-4 space-y-1 text-sm text-gray-600">
          <p>
            <span className="font-medium">Location:</span>{" "}
            {job.locations.join(", ")}
          </p>
          <p>
            <span className="font-medium">Experience:</span>{" "}
            {job.experience || "N/A"}
          </p>
          <p>
            <span className="font-medium">Salary:</span>{" "}
            {job.salary || "Not disclosed"}
          </p>
        </div>

        {/* Action Buttons */}
        <div className="mt-4 flex justify-between items-center">
          <a
            desabled
            // href={job.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline text-sm"
          >
            View Job
          </a>
          <div className="space-x-2">
            {onAddQueue && (
              <button
                onClick={() => onAddQueue(job)}
                disabled={isAlreadyQueued}
                className={`px-2 py-0.5 rounded ${
                  isAlreadyQueued
                    ? "bg-gray-400 cursor-not-allowed text-white"
                    : "bg-green-500 text-white font-normal"
                }`}
              >
                {isAlreadyQueued ? "Alredy Queue" : "Add to Queue"}
              </button>
            )}
            {onApply && (
              <button
                disabled={isApplied || isAlreadyQueued}
                onClick={() => onApply(job)}
                // className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700"
                className={`px-3 py-0.5 rounded ${
                  isApplied || isAlreadyQueued
                    ? "bg-gray-400 cursor-not-allowed text-white"
                    : "bg-green-500 hover:bg-green-600 text-white"
                }`}
              >
                Apply
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobCard;
