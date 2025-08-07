import React from "react";

const JobCard = ({
  job,
  onApply,
  onAddQueue,
  onRemove,
  isQueued,
  isApplied,
}) => {
  return (
    <div className="w-full max-w-sm bg-white shadow-md rounded-lg overflow-hidden border relative">
      {/* Company Logo + Title */}
      <div className="p-4">
        <div className="flex items-center space-x-4">
          <div>
            <div>
              <h3 className="text-lg font-semibold text-gray-800">
                {job.job_title}
              </h3>
              {onRemove && (
                <button
                  onClick={() => onRemove(job)}
                  className="absolute top-2 right-2 text-gray-400 hover:text-red-500 text-lg font-bold"
                >
                  ×
                </button>
              )}
            </div>
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
            href={job.url}
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
                disabled={isQueued}
                className={`px-3 py-1 rounded text-sm ${
                  isQueued
                    ? "bg-gray-400 text-white cursor-not-allowed"
                    : "bg-yellow-400 text-white hover:bg-yellow-500"
                }`}
              >
                {isQueued ? "Queued" : "Add to Queue"}
              </button>
            )}
            {onApply && (
              <button
                onClick={() => onApply(job)}
                disabled={isApplied}
                className={`px-3 py-1 rounded text-sm ${
                  isApplied
                    ? "bg-gray-400 text-white cursor-not-allowed"
                    : "bg-blue-600 text-white hover:bg-blue-700"
                }`}
              >
                {isApplied ? "Applied" : "Apply"}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobCard;
