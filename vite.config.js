import { defineConfig, loadEnv } from 'vite' // Import loadEnv
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => { // Make it a function to access mode
  // Load env variables based on the mode (development, production)
  // This loads from .env files (if present) and process.env.
  // The third argument `''` ensures all env variables are loaded, not just those prefixed with VITE_.
  // Vite will automatically expose VITE_ prefixed variables to client code via import.meta.env,
  // but for `define`, we need to load them manually using loadEnv.
  const env = loadEnv(mode, process.cwd(), '');

  // Prepare Firebase config object from individual VITE_FIREBASE_ variables.
  // These VITE_ prefixed variables are expected to be set in the Docker build environment (from ARGs).
  // Fallback values are provided for local development if .env files or system env vars are not set.
  const firebaseConfig = {
    apiKey: env.VITE_FIREBASE_API_KEY || "YOUR_API_KEY_FALLBACK_VITE",
    authDomain: env.VITE_FIREBASE_AUTH_DOMAIN || "YOUR_AUTH_DOMAIN_FALLBACK_VITE",
    projectId: env.VITE_FIREBASE_PROJECT_ID || "YOUR_PROJECT_ID_FALLBACK_VITE",
    storageBucket: env.VITE_FIREBASE_STORAGE_BUCKET || "YOUR_STORAGE_BUCKET_FALLBACK_VITE",
    messagingSenderId: env.VITE_FIREBASE_MESSAGING_SENDER_ID || "YOUR_MESSAGING_SENDER_ID_FALLBACK_VITE",
    appId: env.VITE_FIREBASE_APP_ID || "YOUR_APP_ID_FALLBACK_VITE", // Firebase App ID
    measurementId: env.VITE_FIREBASE_MEASUREMENT_ID // Optional, no fallback needed if truly optional
  };
  // Remove measurementId if it's not provided and not truly needed as an empty string
  if (!firebaseConfig.measurementId) {
    delete firebaseConfig.measurementId;
  }


  return {
    plugins: [react()],
    server: {
      port: 3000,
      open: true // Automatically open in browser during `npm run dev`
    },
    build: {
      outDir: 'build' // Output directory for `npm run build`
    },
    // Define global constants for client-side code.
    // These values will be replaced directly in the code during the build process.
    // It's crucial that these VITE_ prefixed variables are available during `npm run build`
    // (e.g., set in Dockerfile ENV from ARGs, or in local .env files).
    define: {
      'window.__APP_ID': JSON.stringify(env.VITE_APP_ID || 'your-app-id-vite-fallback'),
      'window.__FIREBASE_CONFIG': JSON.stringify(firebaseConfig),
      'window.__INITIAL_AUTH_TOKEN': JSON.stringify(env.VITE_INITIAL_AUTH_TOKEN || null)
    }
  }
})
