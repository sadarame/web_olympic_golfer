# Vue 3 + TypeScript + Vite

This template should help get you started developing with Vue 3 and TypeScript in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about the recommended Project Setup and IDE Support in the [Vue Docs TypeScript Guide](https://vuejs.org/guide/typescript/overview.html#project-setup).

## Local Development

This project consists of a frontend (Vue.js) and a backend (Firebase Functions). Here's how to run them locally for development.

### Prerequisites

*   Node.js (LTS version recommended)
*   npm (comes with Node.js)
*   Python 3.10 or later
*   pip (comes with Python)
*   Firebase CLI: Install globally using `npm install -g firebase-tools`

### Running the Backend (Firebase Functions) and Serving the Frontend

This method uses the Firebase Emulators to run your backend functions locally and also serves the built frontend application.

1.  **Install Python dependencies for the backend:**
    Navigate to the project root and run:
    ```bash
    pip install -r backend/functions/requirements.txt
    ```

2.  **Start Firebase Emulators:**
    From the project root, run:
    ```bash
    firebase emulators:start
    ```
    This command will start the Firebase Functions emulator (typically on `http://localhost:5001`) and serve the frontend from the `frontend/dist` directory (as configured in `firebase.json`).
    You can access the frontend in your browser at the Hosting URL provided by the emulator (usually `http://localhost:5000`).
    *Note: If you encounter issues with Firebase authentication or permissions for local functions, ensure your Firebase project is properly set up and you are logged in via `firebase login`.*

### Running the Frontend Development Server (for active frontend development)

This method starts a development server for the frontend, allowing for hot-reloading and easier debugging. It will connect to the Firebase Functions emulator if it's running.

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

3.  **Start the frontend development server:**
    ```bash
    npm run dev
    ```
    This will start the frontend development server (typically on `http://localhost:5173`). It is configured to automatically connect to the Firebase Functions emulator running on `http://localhost:5001` when in development mode.