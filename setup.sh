#!/bin/bash

# RayPulse Setup Script
# This script installs dependencies and initializes the database

echo "======================================"
echo "  RayPulse Installation Script"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Download NLTK data
echo ""
echo "Downloading NLTK data..."
python3 -c "import nltk; nltk.download('brown', quiet=True); nltk.download('punkt', quiet=True)"

# Initialize database
echo ""
echo "Initializing database..."
python3 init_db.py

echo ""
echo "======================================"
echo "  Installation Complete!"
echo "======================================"
echo ""
echo "To start RayPulse:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the application: python app.py"
echo "  3. Open browser: http://localhost:5000"
echo ""
echo "======================================"
