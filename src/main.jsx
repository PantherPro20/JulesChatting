// src/main.jsx
// This is the main entry point for the React application.
// It imports the root App component, global styles, and renders the App
// into the DOM element with the ID 'root' found in `public/index.html`.

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css'; // Imports global styles, including Tailwind CSS

// Uses ReactDOM.createRoot for concurrent mode features.
// Renders the App component wrapped in React.StrictMode for development checks.
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
