import React, { useEffect, useRef } from "react";
import JobCard from "../job_card/JobCard";
import { useSelector, useDispatch } from "react-redux";
import { getMatchingJobs, applyJobs } from "../../redux/services/api";
import { addToQueue } from "../../redux/apiSlice";
import { useNavigate } from "react-router-dom";
import ConfirmModal from "../model_alert/ModelAlert";
import { useState } from "react";
const MatchingsPage = () => {
  const dispatch = useDispatch();
  const initialized = useRef(false);
  const nevigate = useNavigate();
  const store_data = useSelector((state) => state.jobsStore);
  const [showConfirm, setShowConfirm] = useState(false);
  // console.log(store_data["loading"]);
  // console.log(store_data.loading);
  function onApply(job) {
    var job_data = [
      {
        job_id: job.id,
        job_title: job.title,
        company_name: job.company_name,
        url: job.url,
      },
    ];
    // dispatch(applyJobs(job_data));
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
  useEffect(() => {
    if (!initialized.current) {
      initialized.current = true;
      dispatch(getMatchingJobs());
    }
  }, [dispatch]);

  return showConfirm ? (
    <ConfirmModal />
  ) : (
    <div className="p-4">
      <h2 className="text-3xl font-bold mb-4 text-center p-5 text-gray-500">
        Matching Jobs
      </h2>
      {store_data.loading ? (
        <p className="text-center font-medium text-1xl text-gray-500">
          wait the data is loading..
        </p>
      ) : (
        ""
      )}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:grid-cols-2 justify-items-center">
        {store_data.matchingJobs.map((job) => (
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

export default MatchingsPage;
