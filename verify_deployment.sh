#!/bin/bash

# Print environment info
echo "Python version:"
python --version

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Run the test script
echo "Running MediaPipe test script..."
python test_mediapipe_version.py

# Check if Flask app can be imported
echo "Checking if Flask app can be initialized..."
python -c "from app import app; print('Flask app initialized successfully')"

echo "Verification complete!" 