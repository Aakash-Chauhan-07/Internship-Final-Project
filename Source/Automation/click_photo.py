import cv2

def click_photo_main():
    # Open the default camera (index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow('Camera', frame)

        # Wait for keypress
        key = cv2.waitKey(1) & 0xFF

        # Check keypress events
        if key == ord('c'):  # Press 'c' to capture photo
            cv2.imwrite(r'Outputs\images\captured_photo.jpg', frame)
            print("Photo captured!")
        elif key == ord('q'):  # Press 'q' to quit
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

