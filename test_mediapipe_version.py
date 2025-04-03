import mediapipe as mp
import cv2
import numpy as np
import os

print(f"MediaPipe version: {mp.__version__}")

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Create a sample blank image for testing
image = np.zeros((480, 640, 3), dtype=np.uint8)
image[:] = (200, 200, 200)  # Gray background

# Draw a simple line to create an image
cv2.line(image, (100, 100), (540, 380), (0, 0, 255), 5)

# Run pose detection on the test image
with mp_pose.Pose(
    static_image_mode=True,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5
) as pose:
    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process the image
    try:
        results = pose.process(image_rgb)
        print("Pose detection successful")
        
        # Check if any landmarks were detected
        if results.pose_landmarks:
            print(f"Detected {len(results.pose_landmarks.landmark)} landmarks")
        else:
            print("No pose landmarks detected in test image (this is expected for a blank image)")
        
    except Exception as e:
        print(f"Error during pose detection: {e}")

print("MediaPipe test completed successfully") 