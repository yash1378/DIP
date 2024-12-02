#!/bin/bash

# Exit immediately if a command exits with a non-zero status, except for specific commands.
set -e

echo "Starting setup for backend and frontend applications..."

# Navigate to the backend directory
echo "Navigating to the backend directory..."
cd backend

echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Starting Flask backend..."
# Run the Flask app in the background
python3 server.py &
BACKEND_PID=$!
echo "Flask backend started with PID $BACKEND_PID"

# Navigate back to the project root
cd ..

# Navigate to the frontend directory
echo "Navigating to the frontend directory..."
cd frontend

echo "Installing Node.js dependencies from package.json..."
npm install --legacy-peer-deps || { echo "Failed to install frontend dependencies"; exit 1; }

echo "Starting Next.js frontend..."
# Run the Next.js app in the background
npm run dev &
FRONTEND_PID=$!
echo "Next.js frontend started with PID $FRONTEND_PID"

echo "Both backend and frontend applications are running!"
echo "Backend: http://127.0.0.1:5000"
echo "Frontend: http://localhost:3000"

# Wait for the backend and frontend processes to exit
trap "kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT SIGTERM

# Keep the script running to ensure both processes stay alive
wait $BACKEND_PID
wait $FRONTEND_PID
