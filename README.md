# Secure & Interactive Web Application

This project is a single-page application (SPA) built with React.js for the frontend and Firebase (Authentication) for backend user management. It features a secure authentication flow with a client-side simulated Two-Factor Authentication (2FA) and an interactive main dashboard. The application is styled with Tailwind CSS and containerized using Docker.

## Core Technologies

*   **Frontend:** React.js (Vite build tool)
*   **Backend Services:** Firebase Authentication (for user sign-up/login)
*   **Styling:** Tailwind CSS
*   **Containerization:** Docker, Docker Compose
*   **Language:** JavaScript (ES6+)

## Key Features

*   **Secure User Authentication:**
    *   Email and Password registration.
    *   User login.
    *   "Forgot Password?" link placeholder.
*   **Client-Side Two-Factor Authentication (2FA):**
    *   Simulated 2FA process after registration and login.
    *   A 6-digit code is "sent" (displayed to the user) for verification.
    *   Disclaimer that this is a simulation for demonstration purposes.
*   **Main Application Dashboard:**
    *   Displays authenticated user's email and UID.
    *   Live, real-time clock updating every second.
    *   Dependent dropdowns for Country and State selection (using local JSON data).
*   **Responsive Design:** Fully responsive UI optimized for desktop, tablet, and mobile devices.
*   **Modern UI/UX:** Clean, intuitive interface with rounded corners on all elements.
*   **Error Handling:** User-friendly error messages displayed within the UI.
*   **Loading States:** Visual feedback during asynchronous operations.

## Project Structure

```
/public/
  index.html          # Main HTML entry point
/src/
  /components/        # React components
    /Auth/            # Authentication related components
    /Dashboard/       # Dashboard related components
  /data/
    locations.json    # Static data for country/state dropdowns
  App.jsx             # Main application component and routing logic
  firebaseConfig.js   # Fallback Firebase configuration
  index.css           # Global styles and Tailwind CSS imports
  main.jsx            # React application entry point
.dockerignore         # Specifies files to ignore in Docker build context
.gitignore            # Specifies intentionally untracked files that Git should ignore
Dockerfile            # Instructions to build the Docker image
LICENSE               # Project License (Assumed MIT, but not explicitly created in this task)
README.md             # This file
docker-compose.yml    # Defines and runs multi-container Docker applications
nginx.conf            # Nginx configuration for serving the SPA
package.json          # Project metadata and dependencies
postcss.config.js     # PostCSS configuration
tailwind.config.js    # Tailwind CSS configuration
vite.config.js        # Vite build tool configuration
```

## Prerequisites

*   **Node.js and npm:** [Download Node.js](https://nodejs.org/) (npm is included).
*   **Docker Desktop:** [Download Docker Desktop](https://www.docker.com/products/docker-desktop) (for Docker-based setup).
*   **Firebase Project:**
    1.  Create a project at [Firebase Console](https://console.firebase.google.com/).
    2.  Enable **Authentication** > **Sign-in method** > **Email/Password**.
    3.  From Project settings, get your Firebase SDK configuration (apiKey, authDomain, etc.).

## Setup and Running Locally (Without Docker)

1.  **Clone/Download the project.**
2.  **Configure Firebase:**
    *   **Option 1 (Recommended for Vite): Create `.env.local` file:**
        In the project root, create a file named `.env.local` and add your Firebase configuration:
        ```env
        VITE_APP_ID=my-local-app
        VITE_FIREBASE_API_KEY=YOUR_API_KEY
        VITE_FIREBASE_AUTH_DOMAIN=YOUR_AUTH_DOMAIN
        VITE_FIREBASE_PROJECT_ID=YOUR_PROJECT_ID
        VITE_FIREBASE_STORAGE_BUCKET=YOUR_STORAGE_BUCKET
        VITE_FIREBASE_MESSAGING_SENDER_ID=YOUR_MESSAGING_SENDER_ID
        VITE_FIREBASE_APP_ID=YOUR_FIREBASE_APP_ID_FROM_SDK
        # VITE_FIREBASE_MEASUREMENT_ID=YOUR_MEASUREMENT_ID (Optional)
        ```
    *   **Option 2 (Directly in `index.html` - less ideal for Vite):**
        Open `public/index.html` and update the `window.__firebase_config` object and `window.__app_id` with your Firebase project details.
3.  **Install Dependencies:**
    ```bash
    npm install
    ```
4.  **Run Development Server:**
    ```bash
    npm run dev
    ```
    The application will typically be available at `http://localhost:3000`.

## Building and Running with Docker

1.  **Clone/Download the project.**
2.  **Configure Firebase for Docker Build:**
    *   **Modify `docker-compose.yml` directly:**
        Edit the `args` section in `docker-compose.yml`. Replace placeholder values (like `YOUR_DOCKER_API_KEY`) with your actual Firebase configuration values. For example:
        ```yaml
        services:
          web:
            build:
              context: .
              dockerfile: Dockerfile
              args:
                REACT_APP_ID: "your-actual-app-id" # Can be any string
                REACT_APP_FIREBASE_API_KEY: "YOUR_ACTUAL_API_KEY"
                REACT_APP_FIREBASE_AUTH_DOMAIN: "YOUR_ACTUAL_AUTH_DOMAIN"
                REACT_APP_FIREBASE_PROJECT_ID: "YOUR_ACTUAL_PROJECT_ID"
                REACT_APP_FIREBASE_STORAGE_BUCKET: "YOUR_ACTUAL_STORAGE_BUCKET"
                REACT_APP_FIREBASE_MESSAGING_SENDER_ID: "YOUR_ACTUAL_MESSAGING_SENDER_ID"
                REACT_APP_FIREBASE_APP_ID: "YOUR_ACTUAL_FIREBASE_APP_ID_FROM_SDK"
                # REACT_APP_FIREBASE_MEASUREMENT_ID: "YOUR_ACTUAL_MEASUREMENT_ID" (Optional)
                # REACT_APP_INITIAL_AUTH_TOKEN: null # Or your token
        ```
    *   **(Alternative) Using Environment Variables in your Shell:**
        Instead of editing `docker-compose.yml` directly, you can set these `REACT_APP_...` variables in your shell environment before running `docker-compose up`. Docker Compose will automatically substitute them if the `args` in `docker-compose.yml` are in the format `VARIABLE_NAME: ${SHELL_VARIABLE_NAME}` or if the shell variable name exactly matches the ARG name. For the current `docker-compose.yml` structure, directly editing or ensuring your shell environment variables match the `REACT_APP_...` names is necessary.
3.  **Build and Run Docker Container:**
    ```bash
    docker-compose up --build
    ```
    The application will be available at `http://localhost` (or the port you mapped if different from 80).
4.  **Stop Docker Container:**
    Press `Ctrl+C` in the terminal where `docker-compose` is running. To remove the containers defined in `docker-compose.yml`, run:
    ```bash
    docker-compose down
    ```

## Firebase Configuration Notes

*   The application is designed to use Firebase's free "Spark Plan." Be mindful of the plan's limitations on reads/writes and storage if extending Firestore usage.
*   Ensure your Firebase project's Authentication (Email/Password) is enabled.
*   The Firebase configuration is primarily injected at build time through Vite's `define` feature, which sources values from environment variables (prefixed with `VITE_` for local dev, or passed as `ARG`s then `ENV` for Docker builds).
*   Fallback configurations are present in `src/firebaseConfig.js` and `vite.config.js` but should ideally be overridden by your actual project configuration for the application to function correctly with your Firebase backend.

## Code Quality

*   **Structure:** Well-structured and modular.
*   **Comments:** Extensively commented.
*   **Error Handling:** User-facing error messages within the UI.
*   **Best Practices:** Follows modern JavaScript/React practices.
```
