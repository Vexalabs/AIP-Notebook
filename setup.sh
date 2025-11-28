#!/bin/bash

echo "🚀 Setting up ML Model Builder Environment (WSL)..."

# 1. Backend Setup
echo "📦 Installing backend dependencies..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# 2. Frontend Setup
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "✅ Setup complete!"
echo "👉 Run './run.sh' to start the application."
