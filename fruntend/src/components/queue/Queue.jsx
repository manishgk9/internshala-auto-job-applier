import React, { useState } from "react";
import JobCard from "../job_card/QueueJobCard";
import { useSelector, useDispatch } from "react-redux";
import { removeFromQueue } from "../../redux/apiSlice";
import { applyJobs } from "../../redux/services/api";
import ConfirmModal from "../model_alert/ModelAlert";
import { useNavigate } from "react-router-dom";
const Queue = () => {
  const dispatch = useDispatch();
  const store_data = useSelector((state) => state.jobsStore);
  const [confirmShow, setConfirmShow] = useState(false);
  const navigate = useNavigate();
  function onApplyAll() {
    var job_data = [];
    store_data.applyQueue.map((item) =>
      job_data.push({
        job_id: item.job_id,
        job_title: item.job_title,
        company_name: item.company_name,
        url: item.url,
      })
    );
    // console.log(job_data);
    dispatch(applyJobs(job_data)).then(() => {
      setConfirmShow(true);
      setTimeout(() => {
        navigate("/applied");
      }, 2000);
    });
  }
  function onApply(job) {
    var job_data = [
      {
        job_id: job.job_id,
        job_title: job.job_title,
        company_name: job.company_name,
        url: job.url,
      },
    ];
    dispatch(applyJobs(job_data)).then(() => {
      setConfirmShow(true);
      setTimeout(() => {
        navigate("/applied");
      }, 2000);
    });
  }
  function onRemove(job) {
    var data = {
      job_id: job.job_id,
      // job_title: job.job_title,
      // company_name: job.company_name,
      // url: job.url,
      // locations: job.locations,
      // salary: job.salary,
      // experience: job.experience,
    };
    console.log(data);
    dispatch(removeFromQueue(data.job_id));
  }
  return confirmShow ? (
    <ConfirmModal />
  ) : (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-6 text-center text-gray-500">
        Queue a list of your jobs
      </h2>

      <div className="flex justify-center mb-6">
        {store_data.applyQueue.length > 1 ? (
          <button
            onClick={onApplyAll}
            className="bg-green-600 text-white px-6 py-1.5 rounded hover:bg-green-700"
          >
            Apply All
          </button>
        ) : (
          ""
        )}
      </div>
      {store_data.applyQueue.length <= 0 ? (
        <p className="text-center font-medium text-1xl text-gray-400">
          Add desigered job position in Queue
        </p>
      ) : (
        ""
      )}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 justify-items-center">
        {store_data.applyQueue.map((job) => (
          <JobCard
            key={job.job_id}
            job={job}
            onApply={onApply}
            onRemove={onRemove}
            minimal={true}
          />
        ))}
      </div>
    </div>
  );
};

export default Queue;
