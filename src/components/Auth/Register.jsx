// src/components/Auth/Register.jsx
// Component for user registration. Handles email/password input,
// password confirmation, basic client-side validation, and Firebase user creation.

import React, { useState } from 'react';
import { getAuth, createUserWithEmailAndPassword } from 'firebase/auth';

// Props:
// - onRegisterSuccess: Function to call when registration and Firebase user creation are successful.
//                      It receives the Firebase user object as an argument.
// - onSwitchToLogin: Function to call to switch the view to the Login component.
// - app: The initialized Firebase app instance, used to get the auth service.
function Register({ onRegisterSuccess, onSwitchToLogin, app }) {
  // State for form inputs
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  // State for displaying errors to the user
  const [error, setError] = useState('');
  // State to manage loading status during Firebase operation, disabling button to prevent multiple submissions
  const [loading, setLoading] = useState(false);

  const auth = getAuth(app);

  // Handles the registration form submission
  const handleRegister = async (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    setError(''); // Clear previous errors

    // Basic client-side validation for password length and confirmation
    if (password.length < 6) {
      setError('Password should be at least 6 characters long.');
      return;
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true); // Indicate that an async operation is starting
    try {
      // Attempt to create a new user with Firebase Authentication
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      onRegisterSuccess(userCredential.user); // Callback on successful registration
    } catch (err) {
      // Handle Firebase errors and provide user-friendly messages
      if (err.code === 'auth/email-already-in-use') {
        setError('This email address is already in use. Please try logging in or use a different email.');
      } else if (err.code === 'auth/weak-password') {
        setError('The password is too weak. Please choose a stronger password (at least 6 characters).');
      } else if (err.code === 'auth/invalid-email') {
        setError('The email address is not valid. Please check and try again.');
      } else {
        // For other Firebase errors, display the default message or a generic one
        setError(err.message || 'Failed to register. Please try again.');
      }
    } finally {
      setLoading(false); // Indicate that the async operation has completed
    }
  };

  return (
    <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-xl shadow-xl">
      <h2 className="text-3xl font-bold text-center text-gray-800">Create Account</h2>
      <form onSubmit={handleRegister} className="space-y-6">
        <div>
          <label htmlFor="email-register" className="block text-sm font-medium text-gray-700">
            Email address
          </label>
          <input
            id="email-register"
            name="email"
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="you@example.com"
          />
        </div>
        <div>
          <label htmlFor="password-register" className="block text-sm font-medium text-gray-700">
            Password (min. 6 characters)
          </label>
          <input
            id="password-register"
            name="password"
            type="password"
            autoComplete="new-password" // Important for password managers
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="••••••••"
          />
        </div>
        <div>
          <label htmlFor="confirm-password-register" className="block text-sm font-medium text-gray-700">
            Confirm Password
          </label>
          <input
            id="confirm-password-register"
            name="confirm-password"
            type="password"
            autoComplete="new-password"
            required
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="••••••••"
          />
        </div>
        {/* Display any error messages */}
        {error && <p className="text-sm text-red-600 bg-red-100 p-3 rounded-md text-center">{error}</p>}
        <div>
          <button
            type="submit"
            disabled={loading} // Disable button when loading
            className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-lg font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {loading ? 'Registering...' : 'Register'}
          </button>
        </div>
      </form>
      <p className="text-sm text-center text-gray-600">
        Already have an account?{' '}
        <button
          onClick={onSwitchToLogin}
          className="font-medium text-blue-600 hover:text-blue-500 focus:outline-none focus:underline"
        >
          Log In
        </button>
      </p>
    </div>
  );
}

export default Register;
