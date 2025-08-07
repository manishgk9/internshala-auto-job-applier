import React from "react";

const AppliedJobCard = ({ job }) => {
  const statusStyles = {
    applying: "text-yellow-600",
    applied: "text-green-600",
    cancelled: "text-red-600",
  };

  return (
    <div className="border rounded-lg p-4 shadow-sm w-full max-w-md bg-white">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-lg font-semibold text-gray-600">
            {job.job_title}
          </h3>
          <p className="text-sm text-gray-600">{job.company_name}</p>
          <p className="text-xs text-gray-400">Job ID: {job.job_id}</p>
        </div>

        <span
          className={`text-sm font-medium ${
            statusStyles[job.status] || "text-gray-500"
          }`}
        >
          {job.status === "applying" ? "⏳ Applying" : "✅ Applied"}
        </span>
      </div>

      {job.appliedAt && (
        <p className="text-xs text-gray-500 mt-2">
          Applied on: {job.applied_on}
        </p>
      )}
    </div>
  );
};

export default AppliedJobCard;
