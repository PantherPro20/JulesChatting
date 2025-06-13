// src/components/Auth/TwoFactorAuth.jsx
// This component simulates a Two-Factor Authentication (2FA) step.
// It generates a client-side code, displays it (simulating an email/SMS),
// and requires the user to enter the code to proceed.
// NOTE: This is a **simulation** for demonstration purposes and does not involve
// actual email/SMS sending or backend 2FA validation.

import React, { useState, useEffect, useCallback } from 'react';

// Props:
// - userEmail: The email address of the user attempting 2FA, displayed in the UI.
// - onVerifySuccess: Function to call when the entered 2FA code is successfully verified.
// - onSignOut: Function to call if the user chooses to cancel 2FA and sign out.
function TwoFactorAuth({ userEmail, onVerifySuccess, onSignOut }) {
  // State for the randomly generated 6-digit code
  const [generatedCode, setGeneratedCode] = useState('');
  // State for the code entered by the user
  const [enteredCode, setEnteredCode] = useState('');
  // State for displaying error messages to the user
  const [error, setError] = useState('');
  // State to manage loading status during verification (simulated)
  const [loading, setLoading] = useState(false);
  // State for messages related to code sending/resending
  const [resendMessage, setResendMessage] = useState('');

  // Generates a new 6-digit code and updates related states.
  // Wrapped in useCallback to stabilize its identity for useEffect dependency.
  const generateCode = useCallback(() => {
    const code = Math.floor(100000 + Math.random() * 900000).toString();
    setGeneratedCode(code);
    // Simulate sending the code: display it to the user for this demo.
    setResendMessage(`For demonstration, your 2FA code is: ${code}`);
    setError(''); // Clear previous errors on new code generation
    setEnteredCode(''); // Clear previous user input
    return code;
  }, []); // No dependencies, so it's created once

  // Generate the initial 2FA code when the component mounts.
  useEffect(() => {
    generateCode();
  }, [generateCode]); // Depends on generateCode (which is stable due to useCallback)

  // Handles the verification of the entered 2FA code.
  const handleVerifyCode = (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Simulate code verification
    if (enteredCode === generatedCode) {
      // In a real application, you might perform additional actions here,
      // like marking 2FA as complete in a backend/Firestore.
      setTimeout(() => { // Simulate network latency for realism
        onVerifySuccess(); // Callback on successful verification
        setLoading(false);
      }, 500);
    } else {
      setError('Invalid 2FA code. Please try again.');
      setLoading(false);
    }
  };

  // Handles the "Resend Code" action.
  const handleResendCode = () => {
    const newCode = generateCode(); // Generate and set a new code
    // Update the message to inform the user (still simulated).
    setResendMessage(`A new 6-digit code has been 'sent'. For demonstration, the code is: ${newCode}`);
  };

  return (
    <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-xl shadow-xl">
      <h2 className="text-2xl font-bold text-center text-gray-800">Two-Factor Authentication</h2>
      <p className="text-center text-gray-600">
        A 6-digit code has been 'sent' to your email ({userEmail}).
      </p>
      {/* Display the simulated email/code message */}
      {resendMessage && (
        <div className="p-3 my-3 text-sm text-blue-700 bg-blue-100 rounded-lg text-center">
          <p className="font-semibold">Important: Simulated Email</p>
          <p>{resendMessage}</p>
          <p className="mt-1 text-xs text-blue-600">
            (In a real application, this code would be sent via a secure backend service.)
          </p>
        </div>
      )}
      <form onSubmit={handleVerifyCode} className="space-y-6">
        <div>
          <label htmlFor="2fa-code" className="block text-sm font-medium text-gray-700">
            Enter 6-digit Code
          </label>
          <input
            id="2fa-code"
            name="2fa-code"
            type="text" // Using text to allow for easy copy-paste; could be "tel" for numeric keyboard
            inputMode="numeric" // Suggests numeric keyboard on mobile
            pattern="\d{6}" // Basic pattern for 6 digits (though validation is manual)
            maxLength="6"
            value={enteredCode}
            onChange={(e) => setEnteredCode(e.target.value.replace(/\D/g, ''))} // Allow only digits
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-center tracking-widest text-lg"
            placeholder="_ _ _ _ _ _"
          />
        </div>
        {/* Display any error messages */}
        {error && <p className="text-sm text-red-600 bg-red-100 p-3 rounded-md text-center">{error}</p>}
        <div>
          <button
            type="submit"
            disabled={loading || enteredCode.length !== 6} // Disable if loading or code is not 6 digits
            className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-lg font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {loading ? 'Verifying...' : 'Verify Code'}
          </button>
        </div>
      </form>
      <div className="text-center">
        <button
          onClick={handleResendCode}
          className="text-sm font-medium text-blue-600 hover:text-blue-500 focus:outline-none focus:underline"
        >
          Resend Code
        </button>
      </div>
       <div className="mt-6 text-center">
        <button
          onClick={onSignOut} // Allow user to cancel and sign out
          className="text-sm font-medium text-gray-600 hover:text-gray-800 underline focus:outline-none focus:text-gray-900"
        >
          Cancel and Sign Out
        </button>
      </div>
    </div>
  );
}

export default TwoFactorAuth;
