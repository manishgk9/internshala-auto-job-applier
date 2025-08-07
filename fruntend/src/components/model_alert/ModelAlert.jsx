import React from "react";

const ConfirmModal = ({ onClose }) => {
  return (
    <div className="fixed inset-0 bg-gray-200    bg-opacity-40 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg p-6 w-80 text-center">
        <h2 className="text-xl font-semibold mb-4">Success!</h2>
        <button
          className="bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600"
          onClick={onClose}
        >
          OK
        </button>
      </div>
    </div>
  );
};

export default ConfirmModal;
