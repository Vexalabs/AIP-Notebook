#!/bin/bash

# Function to kill processes on exit
cleanup() {
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit
}

# Trap Ctrl+C
trap cleanup SIGINT

echo "🚀 Starting ML Model Builder (WSL)..."

# Pre-flight check: Ensure ports are free
echo "Checking for existing processes..."
fuser -k 8000/tcp 2>/dev/null || true
fuser -k 3000/tcp 2>/dev/null || true


# Check and setup backend
echo "Checking Backend dependencies..."
cd backend
if [ ! -d "venv" ]; then
    echo "⚙️  Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing backend dependencies..."
    pip install --upgrade pip
    pip install uvicorn fastapi uvicorn[standard] jupyterlab
    pip install -r requirements.txt 2>/dev/null || echo "Warning: Some requirements failed"
else
    source venv/bin/activate
fi

# Start Backend
echo "Starting Backend (Port 8000)..."
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Check and setup frontend
echo "Checking Frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Start Frontend
echo "Starting Frontend (Port 3000)..."
npm run dev -- --host &
FRONTEND_PID=$!
cd ..

echo "✅ Services started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Press Ctrl+C to stop."

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID
