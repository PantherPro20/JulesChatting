// src/components/Dashboard/Dashboard.jsx
// This component serves as the main view for authenticated users.
// It displays user-specific information, a live time clock, a location selector,
// and provides a way to sign out.

import React from 'react';
import LiveTime from './LiveTime'; // Component to display live time
import LocationSelector from './LocationSelector'; // Component for country/state selection

// Props:
// - user: The authenticated Firebase user object, containing email, UID, etc.
// - onSignOut: Function to call when the user clicks the "Sign Out" button.
function Dashboard({ user, onSignOut }) {
  return (
    <div className="w-full max-w-5xl p-6 sm:p-8 space-y-8 bg-white rounded-xl shadow-2xl">
      {/* Dashboard Header: Welcome message and Sign Out button */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl sm:text-3xl font-bold text-gray-800">Main Application Dashboard</h2>
          {/* Display user's email if available */}
          {user?.email && (
            <p className="text-sm text-gray-500 mt-1">
              Welcome back, <span className="font-semibold text-gray-700">{user.email}</span>!
            </p>
          )}
        </div>
        <button
          onClick={onSignOut}
          className="px-5 py-2.5 text-sm font-medium text-white bg-red-600 rounded-lg shadow-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 transition duration-150 ease-in-out self-start sm:self-center"
        >
          Sign Out
        </button>
      </div>

      {/* User Information Section */}
      {user?.uid && (
        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h3 className="text-md font-semibold text-blue-800">User Information</h3>
          <p className="text-gray-700 text-sm mt-1 break-all"> {/* break-all for long UIDs */}
            User ID: <span className="font-mono bg-blue-100 text-blue-700 px-2 py-0.5 rounded text-xs">{user.uid}</span>
          </p>
        </div>
      )}

      {/* Live Time Display Component */}
      <LiveTime />

      {/* Location Selector Component */}
      <LocationSelector />

    </div>
  );
}

export default Dashboard;
