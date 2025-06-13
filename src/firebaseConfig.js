// ================================================================================================
// !! IMPORTANT !! IMPORTANT !! IMPORTANT !! IMPORTANT !! IMPORTANT !! IMPORTANT !! IMPORTANT !!
// ================================================================================================
//
// THIS FILE CONTAINS **PLACEHOLDER** FIREBASE CONFIGURATION.
//
// YOU **MUST** REPLACE THE VALUES BELOW WITH YOUR ACTUAL FIREBASE PROJECT'S CONFIGURATION
// FOR THE APPLICATION TO WORK CORRECTLY WITH FIREBASE SERVICES.
//
// How to get your Firebase config:
// 1. Go to your Firebase project console (https://console.firebase.google.com/).
// 2. In the project overview, click on "Project settings" (the gear icon).
// 3. Under the "General" tab, scroll down to "Your apps".
// 4. If you haven't registered a web app, click the web icon (</>) to create one.
// 5. Find your web app and copy the `firebaseConfig` object.
//
// This file serves as a **FALLBACK** if the `window.__firebase_config` global variable
// (typically injected by `vite.config.js` from environment variables or during deployment)
// is not available or is incomplete.
//
// ================================================================================================

export const firebaseConfig = {
  apiKey: "YOUR_API_KEY_FALLBACK", // REPLACE WITH YOUR ACTUAL API KEY
  authDomain: "YOUR_AUTH_DOMAIN_FALLBACK", // REPLACE WITH YOUR ACTUAL AUTH DOMAIN
  projectId: "YOUR_PROJECT_ID_FALLBACK", // REPLACE WITH YOUR ACTUAL PROJECT ID
  storageBucket: "YOUR_STORAGE_BUCKET_FALLBACK", // REPLACE WITH YOUR ACTUAL STORAGE BUCKET
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID_FALLBACK", // REPLACE WITH YOUR ACTUAL MESSAGING SENDER ID
  appId: "YOUR_APP_ID_FALLBACK", // REPLACE WITH YOUR ACTUAL APP ID
  measurementId: "YOUR_MEASUREMENT_ID_FALLBACK" // Optional: REPLACE IF YOU USE GOOGLE ANALYTICS
};

// Again, it is CRUCIAL to replace the placeholder values above.
// The application will not function correctly with these placeholders.
// The primary intended method for configuration is via `window.__firebase_config`
// set by Vite during the build process from environment variables.
// This fallback is a last resort and primarily for local development convenience
// if environment variables are not set up.
