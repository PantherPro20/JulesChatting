// src/App.jsx
// This is the root component of the application.
// It manages Firebase initialization, user authentication state, routing between
// authentication screens (choice, login, register, 2FA), and the main dashboard view.
// It also handles global layout elements like header and footer.

import React, { useState, useEffect } from 'react';
import { initializeApp } from 'firebase/app';
import { getAuth, onAuthStateChanged, signOut } from 'firebase/auth';
import { firebaseConfig as fallbackConfig } from './firebaseConfig'; // Fallback Firebase config

// Authentication Components
import AuthChoice from './components/Auth/AuthChoice';
import Register from './components/Auth/Register';
import Login from './components/Auth/Login';
import TwoFactorAuth from './components/Auth/TwoFactorAuth';
// Dashboard Component
import Dashboard from './components/Dashboard/Dashboard';

// Initialize Firebase application.
// It attempts to use configuration from `window.__FIREBASE_CONFIG` (injected by Vite from .env or build script)
// or `window.__firebase_config` (from index.html, less common for Vite) if available and sufficiently populated.
// Otherwise, it falls back to the `fallbackConfig` from `firebaseConfig.js`.
// The check `Object.keys(effectiveConfig).length > 2` is a heuristic to ensure the config object isn't empty or minimal.
const effectiveConfig = (window.__FIREBASE_CONFIG && Object.keys(window.__FIREBASE_CONFIG).length > 2)
  ? window.__FIREBASE_CONFIG
  : (window.__firebase_config && Object.keys(window.__firebase_config).length > 2
      ? window.__firebase_config
      : fallbackConfig);
const app = initializeApp(effectiveConfig);
const auth = getAuth(app); // Get Firebase Auth instance

function App() {
  // State for the currently authenticated Firebase user object. Null if not authenticated.
  const [user, setUser] = useState(null);
  // State for a user who has completed email/password step but not yet 2FA.
  // Helps manage transition to 2FA screen and ensures correct user info is available for 2FA.
  const [pendingUser, setPendingUser] = useState(null);
  // State to track if the application-specific 2FA process has been successfully completed.
  const [is2FAVerified, setIs2FAVerified] = useState(false);
  // State to control which authentication screen is displayed: 'choice', 'login', 'register', or '2fa'.
  const [authScreen, setAuthScreen] = useState('choice');
  // State to manage global loading status, primarily for initial Firebase auth check.
  const [loading, setLoading] = useState(true);
  // State for the application ID, potentially injected via global variable.
  const [appId, setAppId] = useState('');

  // Effect hook for initializing App ID and setting up Firebase auth state listener.
  useEffect(() => {
    // Attempt to set App ID from global variable (e.g., injected by Vite).
    if (window.__APP_ID) {
      setAppId(window.__APP_ID);
    }

    // `onAuthStateChanged` is a Firebase listener that triggers when the user's
    // authentication state changes (login, logout).
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      if (currentUser) {
        // User is signed in according to Firebase.
        // The app's own `is2FAVerified` state will determine if they see the dashboard
        // or are prompted for 2FA again (e.g., if they refreshed on the 2FA page).
        setUser(currentUser);
        // Note: We don't automatically set `is2FAVerified` to true here.
        // That state is managed by the `handle2FAVerifySuccess` function.
        // If `pendingUser` is null and `currentUser` exists, it might mean the user
        // refreshed while on the 2FA page or is returning. The `getAuthComponent`
        // logic will correctly show 2FA if `is2FAVerified` is still false.
      } else {
        // User is signed out. Reset all authentication-related states.
        setUser(null);
        setPendingUser(null);
        setIs2FAVerified(false);
        setAuthScreen('choice'); // Default to auth choice screen on logout.
      }
      setLoading(false); // Finished initial auth check.
    });

    // Cleanup function: Unsubscribe from the listener when the component unmounts
    // to prevent memory leaks.
    return () => unsubscribe();
  }, []); // Empty dependency array: runs once on mount, cleans up on unmount.

  // Handles user sign-out.
  const handleSignOut = async () => {
    setLoading(true); // Show loading state during sign-out process.
    try {
      await signOut(auth); // Firebase sign-out.
      // `onAuthStateChanged` listener will handle resetting user state and navigating to 'choice'.
    } catch (error) {
      console.error("Error signing out: ", error);
      // Optionally, display a user-facing error message here.
      // For now, state reset is handled by onAuthStateChanged or finally block.
    } finally {
      // Explicitly reset all auth-related states here as a safeguard,
      // though onAuthStateChanged should also cover this.
      setUser(null);
      setPendingUser(null);
      setIs2FAVerified(false);
      setAuthScreen('choice');
      setLoading(false);
    }
  };

  // Handles user's choice on the AuthChoice screen ('login' or 'register').
  const handleAuthChoice = (choice) => {
    setAuthScreen(choice);
    setErrorForAuthScreen(''); // Clear any previous errors when switching screens
  };

  // Clears error for the specific auth screen (Login or Register)
  // This is a helper to be called when switching between login/register or on successful operations.
  // Note: This assumes Login and Register components lift their setError function or handle it internally.
  // For this iteration, error state is managed within Login/Register components, so this function is conceptual
  // unless those components are refactored to have errors managed by App.jsx.
  // We will rely on internal error clearing for now.
  const setErrorForAuthScreen = (message) => {
    // This function would interact with error states if they were lifted to App.jsx
    // console.log("setErrorForAuthScreen called with:", message);
  };


  // Callback for successful user registration (after Firebase createUser).
  // Sets the newly registered user as 'pending' and navigates to 2FA screen.
  const handleRegisterSuccess = (registeredUser) => {
    setPendingUser(registeredUser);
    setAuthScreen('2fa');
  };

  // Callback for successful user login (after Firebase signIn).
  // Sets the logged-in user as 'pending' and navigates to 2FA screen.
  const handleLoginSuccess = (loggedInUser) => {
    setPendingUser(loggedInUser);
    setAuthScreen('2fa');
  };

  // Callback for successful 2FA verification.
  // Promotes the `pendingUser` to `user` (if applicable, primarily for first-time 2FA)
  // and marks 2FA as verified.
  const handle2FAVerifySuccess = () => {
    if (pendingUser) {
      setUser(pendingUser); // Solidify the user state with the one from login/registration.
      // setPendingUser(null); // Clear pendingUser as they are now fully authenticated.
    }
    // If pendingUser is null, it implies `onAuthStateChanged` already set the `user`
    // (e.g., user refreshed on 2FA page). We are just completing 2FA for that `user`.
    setIs2FAVerified(true);
    // No need to change authScreen here; rendering logic in `getAuthComponent` handles it.
  };

  // Global loading screen while checking initial Firebase auth state.
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <div className="p-10 rounded-xl shadow-2xl bg-white">
           <svg className="animate-spin h-10 w-10 text-blue-600 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p className="text-xl text-gray-700">Loading Application...</p>
        </div>
      </div>
    );
  }

  // Determines which component to render based on authentication state.
  const getAuthComponent = () => {
    // If a Firebase user exists AND 2FA has been verified, show the Dashboard.
    if (user && is2FAVerified) {
      return <Dashboard user={user} onSignOut={handleSignOut} />;
    }

    // If a user is set (by Firebase auth) OR a `pendingUser` exists (just passed email/pass step)
    // AND the current screen is '2fa', show the TwoFactorAuth component.
    // The `userEmail` prop prioritizes `pendingUser`'s email if available.
    if ((user || pendingUser) && authScreen === '2fa') {
       return <TwoFactorAuth
                userEmail={pendingUser?.email || user?.email} // Pass email for display
                onVerifySuccess={handle2FAVerifySuccess}
                onSignOut={handleSignOut} // Allow signing out from 2FA screen
              />;
    }

    // Otherwise, show the appropriate authentication screen (choice, login, or register).
    switch (authScreen) {
      case 'login':
        return <Login onLoginSuccess={handleLoginSuccess} onSwitchToRegister={() => { setAuthScreen('register'); setErrorForAuthScreen(''); }} app={app} />;
      case 'register':
        return <Register onRegisterSuccess={handleRegisterSuccess} onSwitchToLogin={() => { setAuthScreen('login'); setErrorForAuthScreen(''); }} app={app} />;
      case 'choice':
      default:
        return <AuthChoice onChoice={handleAuthChoice} />;
    }
  };

  // Main application layout.
  return (
    <div className="App min-h-screen bg-gray-100 flex flex-col items-center justify-center text-gray-800 selection:bg-blue-200">
      <header className="App-header px-4 py-3 sm:px-5 sm:py-4 bg-blue-600 text-white w-full text-center shadow-md rounded-b-xl fixed top-0 left-0 right-0 z-10">
        <h1 className="text-2xl sm:text-3xl font-bold">Secure Interactive Web Application</h1>
        {appId && <p className="text-xs sm:text-sm mt-1">App ID: <span className="font-mono">{appId}</span></p>}
      </header>
      {/* Main content area where the conditionally rendered component (auth or dashboard) is displayed. */}
      <main className="flex-grow container mx-auto p-4 sm:p-6 md:p-8 w-full flex items-center justify-center pt-20 sm:pt-24"> {/* Adjusted pt for new header padding */}
        {getAuthComponent()}
      </main>
      <footer className="w-full text-center p-3 sm:p-4 text-xs sm:text-sm text-gray-600 border-t border-gray-300 bg-gray-50 rounded-t-xl">
        <p>&copy; {new Date().getFullYear()} Secure App. All rights reserved. For demonstration purposes.</p>
      </footer>
    </div>
  );
}

export default App;
