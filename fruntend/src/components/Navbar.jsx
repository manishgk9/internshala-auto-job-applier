import React, { useState } from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <div className="bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex justify-between items-center">
        {/* Brand */}
        <div className="text-xl font-bold text-gray-500">
          Internshala Auto Applyer
        </div>

        {/* Desktop Nav Links */}
        <div className="hidden md:flex items-center space-x-6">
          <Link to="/" className="text-gray-600 hover:text-blue-500">
            Matchings
          </Link>
          <Link to="/search" className="text-gray-600 hover:text-blue-500">
            Search
          </Link>
          <Link to="/queue" className="text-gray-600 hover:text-blue-500">
            Queue
          </Link>
          <Link to="/applied" className="text-gray-600 hover:text-blue-500">
            Applied
          </Link>
        </div>

        {/* Hamburger Icon */}
        <div className="md:hidden">
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="text-gray-700 focus:outline-none"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              {isMenuOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Nav */}
      {isMenuOpen && (
        <div className="md:hidden px-4 pb-4 space-y-2">
          <Link to="/" className="block text-gray-600">
            Matchings
          </Link>
          <Link to="/search" className="block text-gray-600">
            Search
          </Link>
          <Link to="/queue" className="block text-gray-600">
            Queue
          </Link>
          <Link to="/applied" className="block text-gray-600">
            Applied
          </Link>
        </div>
      )}
    </div>
  );
};

export default Navbar;
