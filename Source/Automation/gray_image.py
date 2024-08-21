import cv2
import os
import numpy as np

def capture_and_process_image():
    # Capture image from webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Failed to open webcam")
        return
    
    while True:
        # Capture a single frame
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to capture image")
            break
        
        # Convert the captured frame to grayscale
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Display the images
        cv2.imshow('Grayscale Image', gray_image)
        
        # Wait for key press
        key = cv2.waitKey(1) & 0xFF
        
        # If 'c' is pressed, save the grayscale image
        if key == ord('c'):
            gray_image_path = rf"Outputs\images\gray_image{np.random.randint(1, 100)}.jpg"  # Replace with your desired file path
            os.makedirs(os.path.dirname(gray_image_path), exist_ok=True)
            cv2.imwrite(gray_image_path, gray_image)
            print(f"Grayscale image saved at {gray_image_path}")
        
        # If 'q' is pressed, exit the loop
        elif key == ord('q'):
            break
    
    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()


