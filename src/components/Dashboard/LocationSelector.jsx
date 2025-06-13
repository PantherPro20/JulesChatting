// src/components/Dashboard/LocationSelector.jsx
// This component allows users to select a country and then a state/region/province
// from predefined lists loaded from a JSON file.

import React, { useState, useEffect } from 'react';
import locationData from '../../data/locations.json'; // Static data for countries and states

function LocationSelector() {
  // State to hold the list of countries, initialized from the imported JSON data
  const [countries] = useState(locationData.countries);
  // State for the currently selected country name
  const [selectedCountry, setSelectedCountry] = useState('');
  // State to hold the list of states for the currently selected country
  const [states, setStates] = useState([]);
  // State for the currently selected state name
  const [selectedState, setSelectedState] = useState('');

  // Effect to update the list of states when the selectedCountry changes.
  useEffect(() => {
    if (selectedCountry) {
      // Find the selected country object from the countries list
      const country = countries.find(c => c.name === selectedCountry);
      // Set the states for the dropdown; if country not found or has no states, defaults to empty array
      setStates(country ? country.states : []);
      setSelectedState(''); // Reset state selection when country changes
    } else {
      // If no country is selected, clear the states list and selection
      setStates([]);
      setSelectedState('');
    }
  }, [selectedCountry, countries]); // Dependencies: runs when selectedCountry or countries list changes

  // Handles changes to the country selection dropdown.
  const handleCountryChange = (e) => {
    setSelectedCountry(e.target.value);
    // State selection is reset via the useEffect hook triggered by selectedCountry change
  };

  // Handles changes to the state selection dropdown.
  const handleStateChange = (e) => {
    setSelectedState(e.target.value);

    // Placeholder for potential data saving logic (e.g., to Firestore).
    // For this application, we are just logging the selection to the console.
    // If implementing Firestore writes, be mindful of write limits, especially on free tiers.
    if (e.target.value) {
      console.log(`Selected location: State/Region - ${e.target.value}, Country - ${selectedCountry}`);
    }
  };

  return (
    <div className="p-6 bg-white rounded-xl shadow-lg space-y-6">
      <h3 className="text-xl font-semibold text-gray-700 mb-4">Select Your Location</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Country Dropdown */}
        <div>
          <label htmlFor="country-select" className="block text-sm font-medium text-gray-700 mb-1">
            Country
          </label>
          <select
            id="country-select"
            value={selectedCountry}
            onChange={handleCountryChange}
            className="mt-1 block w-full pl-3 pr-10 py-2.5 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md shadow-sm bg-white"
          >
            <option value="">Select a Country</option>
            {countries.map((country) => (
              <option key={country.name} value={country.name}>
                {country.name}
              </option>
            ))}
          </select>
        </div>
        {/* State/Region/Province Dropdown */}
        <div>
          <label htmlFor="state-select" className="block text-sm font-medium text-gray-700 mb-1">
            State/Region/Province
          </label>
          <select
            id="state-select"
            value={selectedState}
            onChange={handleStateChange}
            disabled={!selectedCountry || states.length === 0} // Disable if no country selected or no states available
            className="mt-1 block w-full pl-3 pr-10 py-2.5 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md shadow-sm bg-white disabled:bg-gray-100 disabled:cursor-not-allowed"
          >
            <option value="">
              {selectedCountry ? (states.length > 0 ? 'Select a State' : 'No states available') : 'Select a Country First'}
            </option>
            {states.map((state) => (
              <option key={state} value={state}>
                {state}
              </option>
            ))}
          </select>
        </div>
      </div>
      {/* Display the selected location */}
      {selectedCountry && selectedState && (
        <p className="mt-4 text-sm text-gray-600">
          Your selected location: <span className="font-semibold">{selectedState}, {selectedCountry}</span>
        </p>
      )}
    </div>
  );
}

export default LocationSelector;
