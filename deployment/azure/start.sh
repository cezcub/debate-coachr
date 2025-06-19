#!/bin/bash

# Exit on any error
set -e

echo "Starting Coachr AI services..."

# Start FastAPI backend in background
echo "Starting FastAPI backend on port 8000..."
uvicorn backend.backend:app --host 0.0.0.0 --port 8000 &

# Wait a moment for backend to start
sleep 3

# Start Streamlit frontend
echo "Starting Streamlit frontend on port 8501..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true --server.enableCORS false

# Keep the script running
wait