// import React from "react";
import { useNavigate } from "react-router-dom";

function WelcomePage() {
  const navigate = useNavigate();

  return (
    <div className="bg-white flex flex-col items-center justify-center p-10 shadow-xl rounded-lg w-full max-w-md">
      <h2 className="text-3xl font-bold text-gray-800 mb-2 text-center">
        Welcome to Cricket Coach
      </h2>
      <p className="text-lg text-gray-600 text-center mb-4">
        AI Powered Cricket Coaching
      </p>
      <img src="./Welcome logo.png" alt="Cricket Logo" className="w-40 mb-4" />
      <button
        className="mt-4 bg-green-700 text-white px-6 py-2 rounded-full text-lg hover:bg-green-800 transition"
        onClick={() => navigate("/signin")}
      >
        Sign in
      </button>
    </div>
  );
}

export default WelcomePage;
