import React, { useEffect, useRef } from "react";
import AppliedJobCard from "../job_card/AppliedCardJob";
import { useDispatch, useSelector } from "react-redux";
import { appliedJobs } from "../../redux/services/api";
const Applied = () => {
  const dispatch = useDispatch();
  const initialized = useRef(false);
  const store_data = useSelector((state) => state.jobsStore);
  useEffect(() => {
    if (!initialized.current) {
      initialized.current = true;
      dispatch(appliedJobs());
    }
  }, [dispatch]);

  function onRefresh() {
    dispatch(appliedJobs());
  }
  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-6 text-center text-gray-500">
        Your applied or proccessing Jobs are here{" "}
        <button onClick={onRefresh} className="font-mono text-xl underline">
          refresh
        </button>
      </h2>

      {store_data.loading ? (
        <p className="text-center font-medium text-1xl text-gray-500">
          wait your search loading..
        </p>
      ) : store_data.appliedJobs.length == 0 ? (
        <p className="text-center font-medium text-1xl text-gray-400">
          No active or proccessing data is available
        </p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 justify-items-center">
          {store_data.appliedJobs.map((job) => (
            <AppliedJobCard key={job.job_id} job={job} />
          ))}
        </div>
      )}
    </div>
  );
};

export default Applied;
