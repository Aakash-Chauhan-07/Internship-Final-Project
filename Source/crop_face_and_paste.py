import cv2
import streamlit as st
import numpy as np
from PIL import Image
import io

# Load Haar Cascade for face detection
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

# Function to capture an image from the webcam
def capture_image(image_path='captured_image.jpg'):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Could not open webcam")
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        st.error("Failed to capture image")
        return None

    cv2.imwrite(image_path, frame)
    return image_path

# Function to load and process the image
def load_and_process_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        st.error("Failed to load image.")
        return None

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        st.warning("No faces detected")
        return image

    x, y, w, h = faces[0]
    face = image[y:y+h, x:x+w]

    face_resized = cv2.resize(face, (w, h))
    image[0:h, 0:w] = face_resized
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Convert BGR to RGB for display in Streamlit
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image_rgb

# Streamlit app
def process():
    st.title("Face Detection and Cropping Tool")

    # Handle session state for image capture
    if "image_path" not in st.session_state:
        st.session_state.image_path = None
        st.session_state.image_captured = False

    # Button to capture or re-capture the image
    if st.button("Capture Photo"):
        st.session_state.image_path = capture_image('captured_image.jpg')
        if st.session_state.image_path:
            st.session_state.image_captured = True

    # Show image if it has been captured
    if st.session_state.image_captured:
        processed_image = load_and_process_image(st.session_state.image_path)
        if processed_image is not None:
            st.image(processed_image, caption="Processed Image", use_column_width=True)

            # Provide a download button for the processed image
            pil_image = Image.fromarray(processed_image)
            buffered = io.BytesIO()
            pil_image.save(buffered, format="JPEG")
            st.download_button(label="Download Processed Image", data=buffered.getvalue(), file_name='processed_image.jpg', mime='image/jpeg')

if __name__ == "__main__":
    process()
    