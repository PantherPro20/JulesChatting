// src/components/Auth/AuthChoice.jsx
// This component provides users with the initial choice to either
// navigate to the registration form or the login form.

import React from 'react';

// Props:
// - onChoice: Function to call when the user selects an option.
//             It receives either 'register' or 'login' as an argument.
function AuthChoice({ onChoice }) {
  return (
    <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-xl shadow-xl">
      <h2 className="text-3xl font-bold text-center text-gray-800">Welcome!</h2>
      <p className="text-center text-gray-600">Please choose an option to continue.</p>
      <div className="flex flex-col space-y-4 sm:flex-row sm:space-y-0 sm:space-x-4">
        {/* Button to navigate to the registration form */}
        <button
          onClick={() => onChoice('register')}
          className="w-full px-4 py-3 text-lg font-semibold text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition duration-150 ease-in-out"
        >
          Create an Account
        </button>
        {/* Button to navigate to the login form */}
        <button
          onClick={() => onChoice('login')}
          className="w-full px-4 py-3 text-lg font-semibold text-white bg-green-600 rounded-lg shadow-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 transition duration-150 ease-in-out"
        >
          Log In
        </button>
      </div>
    </div>
  );
}

export default AuthChoice;
