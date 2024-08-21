import cv2
import numpy as np

def filter():
    # Load the Haar Cascade classifiers for face and eye detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Load the overlay image (sunglasses) with an alpha channel
    overlay_image = cv2.imread(r"sunglass.png", cv2.IMREAD_UNCHANGED)

    # Capture video from the webcam
    cap = cv2.VideoCapture(0)
    frame_counter = 0  # Counter for saved frames

    # Start the main loop
    while True:
        status, frame = cap.read()
    
        # Check if the frame was captured successfully
        if not status:
            print("Failed to capture image")
            break

        # Convert the frame to grayscale
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale image
        faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Process each detected face
        for (x, y, w, h) in faces:
            # Extract the region of interest (ROI) for the face
            roi_gray = gray_img[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            # Detect eyes within the face ROI
            eyes = eye_cascade.detectMultiScale(roi_gray)

            # Process the detected eyes
            if len(eyes) > 0:
                # Calculate the bounding box that covers all the detected eyes
                ex_min, ey_min = eyes[0][:2]
                ex_max, ey_max = eyes[0][:2]
                ew_max, eh_max = eyes[0][2:]

                for (ex, ey, ew, eh) in eyes:
                    ex_min = min(ex_min, ex)
                    ey_min = min(ey_min, ey)
                    ex_max = max(ex_max, ex + ew)
                    ey_max = max(ey_max, ey + eh)

                # Determine the width and height for the overlay image
                overlay_width = ex_max - ex_min
                overlay_height = ey_max - ey_min

                # Resize the overlay image to fit within the bounding box
                resized_overlay = cv2.resize(overlay_image, (overlay_width, overlay_height), interpolation=cv2.INTER_AREA)

                # Extract the alpha channel from the resized overlay
                if resized_overlay.shape[2] == 4:  # Ensure the overlay has an alpha channel
                    alpha_mask = resized_overlay[:, :, 3] / 255.0
                    alpha_inv = 1.0 - alpha_mask

                    for c in range(0, 3):  # Iterate over each color channel
                        roi_color[ey_min:ey_min+overlay_height, ex_min:ex_min+overlay_width, c] = (
                            alpha_mask * resized_overlay[:, :, c] + alpha_inv * roi_color[ey_min:ey_min+overlay_height, ex_min:ex_min+overlay_width, c]
                        )

        # Display the processed frame
        cv2.imshow('Face and Eye Detection', frame)

        # Exit the loop on 'q' key press or save frame on 'c' key press
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            # Save the current frame
            frame_filename = f'frame_{frame_counter}.png'
            cv2.imwrite(frame_filename, frame)
            print(f'Saved {frame_filename}')
            frame_counter += 1

    # Release the video capture and close windows
    cap.release()
    cv2.destroyAllWindows()

