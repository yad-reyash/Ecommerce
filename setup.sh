#!/bin/bash

# E-commerce Application Setup Script

echo "🚀 Setting up E-commerce Application..."
echo ""

# Backend setup
echo "📦 Setting up Django Backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate

echo ""
echo "✅ Backend setup complete!"
echo ""

# Frontend setup
cd ../frontend
echo "📦 Setting up React Frontend..."

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

echo ""
echo "✅ Frontend setup complete!"
echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To run the application:"
echo "  Backend:  cd backend && source venv/bin/activate && python manage.py runserver"
echo "  Frontend: cd frontend && npm run dev"
echo ""
