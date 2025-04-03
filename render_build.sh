#!/bin/bash
# This is a custom build script for Render deployment

# Install dependencies with specific pip options to avoid conflicts
pip install --upgrade pip
pip install -r requirements.txt

# Print versions for debugging
echo "========== Environment Info =========="
python --version
pip --version
echo "OpenCV version:"
python -c "import cv2; print(cv2.__version__)"
echo "MediaPipe version:"
python -c "import mediapipe as mp; print(mp.__version__)"
echo "====================================="

# Make sure script is executable
chmod +x verify_deployment.sh

# Run the verification script
./verify_deployment.sh

echo "Build completed successfully!" 