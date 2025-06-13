// src/components/Dashboard/LiveTime.jsx
// This component displays the current local time and date, updating every second.

import React, { useState, useEffect } from 'react';

function LiveTime() {
  // State to hold the current time
  const [currentTime, setCurrentTime] = useState(new Date());

  // Effect to set up and clean up the interval timer for time updates.
  useEffect(() => {
    // Set an interval to update the currentTime every 1000ms (1 second)
    const timerId = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    // Cleanup function: clear the interval when the component unmounts
    // to prevent memory leaks and unnecessary updates.
    return () => clearInterval(timerId);
  }, []); // Empty dependency array means this effect runs once on mount and cleans up on unmount.

  // Formats the date object into a readable string: "HH:MM:SS AM/PM, Day, Month DD, YYYY"
  const formatTime = (date) => {
    let hours = date.getHours();
    const minutes = date.getMinutes().toString().padStart(2, '0'); // Ensure two digits
    const seconds = date.getSeconds().toString().padStart(2, '0'); // Ensure two digits
    const ampm = hours >= 12 ? 'PM' : 'AM';

    hours = hours % 12;
    hours = hours ? hours : 12; // Convert hour '0' (midnight) to '12'
    const strTime = `${hours.toString().padStart(2, '0')}:${minutes}:${seconds} ${ampm}`;

    // Get textual representation of day and month
    const day = date.toLocaleDateString(undefined, { weekday: 'long' });
    const month = date.toLocaleDateString(undefined, { month: 'long' });
    const dayOfMonth = date.getDate();
    const year = date.getFullYear();

    return `${strTime}, ${day}, ${month} ${dayOfMonth}, ${year}`;
  };

  return (
    <div className="p-4 bg-gray-50 rounded-lg shadow text-center">
      <p className="text-xl sm:text-2xl font-semibold text-blue-700">
        {/* Display the formatted current time */}
        {formatTime(currentTime)}
      </p>
    </div>
  );
}

export default LiveTime;
