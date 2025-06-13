// src/components/Auth/Login.jsx
// Component for user login. Handles email/password input and Firebase user authentication.

import React, { useState } from 'react';
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth';

// Props:
// - onLoginSuccess: Function to call when login is successful.
//                   It receives the Firebase user object as an argument.
// - onSwitchToRegister: Function to call to switch the view to the Register component.
// - app: The initialized Firebase app instance, used to get the auth service.
function Login({ onLoginSuccess, onSwitchToRegister, app }) {
  // State for form inputs
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // State for displaying errors to the user
  const [error, setError] = useState('');
  // State to manage loading status during Firebase operation, disabling button to prevent multiple submissions
  const [loading, setLoading] = useState(false);

  const auth = getAuth(app);

  // Handles the login form submission
  const handleLogin = async (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    setError(''); // Clear previous errors
    setLoading(true); // Indicate that an async operation is starting

    try {
      // Attempt to sign in the user with Firebase Authentication
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      onLoginSuccess(userCredential.user); // Callback on successful login
    } catch (err) {
      // Handle Firebase errors and provide user-friendly messages
      if (err.code === 'auth/user-not-found' || err.code === 'auth/wrong-password' || err.code === 'auth/invalid-credential') {
        setError('Invalid email or password. Please try again.');
      } else if (err.code === 'auth/invalid-email') {
        setError('The email address is not valid. Please check and try again.');
      } else if (err.code === 'auth/too-many-requests') {
        setError('Access to this account has been temporarily disabled due to many failed login attempts. You can try again later.');
      }
       else {
        // For other Firebase errors, display the default message or a generic one
        setError(err.message || 'Failed to log in. Please try again.');
      }
    } finally {
      setLoading(false); // Indicate that the async operation has completed
    }
  };

  return (
    <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-xl shadow-xl">
      <h2 className="text-3xl font-bold text-center text-gray-800">Log In</h2>
      <form onSubmit={handleLogin} className="space-y-6">
        <div>
          <label htmlFor="email-login" className="block text-sm font-medium text-gray-700">
            Email address
          </label>
          <input
            id="email-login"
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
          <label htmlFor="password-login" className="block text-sm font-medium text-gray-700">
            Password
          </label>
          <input
            id="password-login"
            name="password"
            type="password"
            autoComplete="current-password" // Important for password managers
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="••••••••"
          />
        </div>
        {/* Display any error messages */}
        {error && <p className="text-sm text-red-600 bg-red-100 p-3 rounded-md text-center">{error}</p>}
        <div className="flex items-center justify-between">
          <div className="text-sm">
            {/* Placeholder for Forgot Password functionality */}
            <a href="#" className="font-medium text-blue-600 hover:text-blue-500 focus:outline-none focus:underline">
              Forgot Password?
            </a>
          </div>
        </div>
        <div>
          <button
            type="submit"
            disabled={loading} // Disable button when loading
            className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-lg font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
          >
            {loading ? 'Logging In...' : 'Log In'}
          </button>
        </div>
      </form>
      <p className="text-sm text-center text-gray-600">
        Don't have an account?{' '}
        <button
          onClick={onSwitchToRegister}
          className="font-medium text-blue-600 hover:text-blue-500 focus:outline-none focus:underline"
        >
          Create an Account
        </button>
      </p>
    </div>
  );
}

export default Login;
