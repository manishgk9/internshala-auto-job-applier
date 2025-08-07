import React from "react";

const Dashboard = ({ appliedJobs }) => {
  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Application Status</h2>
      {appliedJobs.map((job) => (
        <div
          key={job.id}
          className="border-b pb-2 mb-2 flex justify-between items-center"
        >
          <div>
            <h4 className="font-semibold">{job.title}</h4>
            <p className="text-sm text-gray-500">{job.company}</p>
          </div>
          <span className="text-green-600">Applied</span>
        </div>
      ))}
    </div>
  );
};

export default Dashboard;
