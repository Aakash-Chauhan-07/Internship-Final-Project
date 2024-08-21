import cv2
import numpy as np
import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import io

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

def apply_filter(image, filter_type):
    pil_image = Image.fromarray(image)
    
    if filter_type == 'Gray':
        pil_image = ImageOps.grayscale(pil_image)
    elif filter_type == 'Hot':
        gray_image = ImageOps.grayscale(pil_image)
        pil_image = ImageOps.colorize(gray_image, black="black", white="lightsalmon")
    elif filter_type == 'Cold':
        # Apply a subtle cold effect by increasing the blue component
        img_np = np.array(pil_image.convert('RGB'))
        img_np[..., 0] = np.clip(img_np[..., 0] + 20, 0, 255)  # Increase blue channel
        pil_image = Image.fromarray(img_np)
    elif filter_type == 'Stars':
        draw = ImageDraw.Draw(pil_image)
        width, height = pil_image.size
        num_stars = 50
        for _ in range(num_stars):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            size = np.random.randint(10, 30)
            color = (255, 255, 0)  # Yellow color for stars
            draw_star(draw, (x, y), size, color)
    elif filter_type == 'Negative':
        pil_image = ImageOps.invert(pil_image.convert('RGB'))

    return np.array(pil_image)

def draw_star(draw, center, size, color):
    x, y = center
    points = [
        (x, y - size), 
        (x + size * 0.2245, y - size * 0.309), 
        (x + size, y - size * 0.309), 
        (x + size * 0.3633, y + size * 0.118), 
        (x + size * 0.5878, y + size * 0.809), 
        (x, y + size * 0.382), 
        (x - size * 0.5878, y + size * 0.809), 
        (x - size * 0.3633, y + size * 0.118), 
        (x - size, y - size * 0.309), 
        (x - size * 0.2245, y - size * 0.309)
    ]
    draw.polygon(points, outline=color, fill=color)

def main():
    st.title("Image Filter Tool")

    if "image_path" not in st.session_state:
        st.session_state.image_path = None
        st.session_state.image_captured = False

    if st.button("Capture Photo"):
        st.session_state.image_path = capture_image('captured_image.jpg')
        if st.session_state.image_path:
            st.session_state.image_captured = True

    if st.session_state.image_captured:
        # Load and convert image
        image = cv2.imread(st.session_state.image_path)
        if image is not None:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            filter_type = st.selectbox("Choose a filter", ["Gray", "Hot", "Cold", "Stars", "Negative"])
            filtered_image = apply_filter(image_rgb, filter_type)

            st.image(filtered_image, caption=f"Image with {filter_type} Filter", use_column_width=True)

            pil_image = Image.fromarray(filtered_image)
            buffered = io.BytesIO()
            pil_image.save(buffered, format="JPEG")
            st.download_button(label="Download Processed Image", data=buffered.getvalue(), file_name=f'{filter_type.lower()}_filtered_image.jpg', mime='image/jpeg')

if __name__ == "__main__":
    main()
    