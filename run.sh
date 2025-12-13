#!/bin/bash

# Script to run both frontend and backend servers

echo "🚀 Starting E-commerce Application..."
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend
echo "📦 Starting Django Backend on http://localhost:8000..."
cd backend

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    source venv/bin/activate
    python manage.py runserver > /tmp/backend.log 2>&1 &
    BACKEND_PID=$!
else
    # Use python3 if no venv exists
    python3 manage.py runserver > /tmp/backend.log 2>&1 &
    BACKEND_PID=$!
fi
cd ..

sleep 2

# Check if backend started successfully
if ps -p $BACKEND_PID > /dev/null; then
    echo "✅ Backend started successfully (PID: $BACKEND_PID)"
else
    echo "❌ Failed to start backend"
    exit 1
fi

# Start frontend
echo "📦 Starting React Frontend on http://localhost:5173..."
cd frontend
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

sleep 2

# Check if frontend started successfully
if ps -p $FRONTEND_PID > /dev/null; then
    echo "✅ Frontend started successfully (PID: $FRONTEND_PID)"
else
    echo "❌ Failed to start frontend"
    kill $BACKEND_PID
    exit 1
fi

echo ""
echo "🎉 Application is running!"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo "   Admin:    http://localhost:8000/admin"
echo ""
echo "Press Ctrl+C to stop both servers..."
echo ""

# Keep script running
wait
