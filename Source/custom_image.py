import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import io

def custom_image():
    def create_collage(images, num_images):
        if num_images not in [4, 9]:
            st.error("Number of images must be 4 or 9.")
            return None

        # Determine grid size and collage dimensions based on the number of images
        if num_images == 4:
            grid_size = 2
        elif num_images == 9:
            grid_size = 3

        collage_width = 800
        collage_height = 800
        cell_size = min(collage_width // grid_size, collage_height // grid_size)

        # Create a custom background using NumPy
        background_array = np.zeros((collage_height, collage_width, 3), dtype=np.uint8)

        # Example of a custom background with a gradient (modify as needed)
        for i in range(collage_height):
            background_array[i, :] = [int(255 * i / collage_height), int(255 * (collage_height - i) / collage_height), 128]

        # Convert the NumPy array to a PIL image
        collage = Image.fromarray(background_array)

        # Resize and paste images into the collage
        for i in range(num_images):
            img = images[i].resize((cell_size, cell_size), Image.LANCZOS)
            x = (i % grid_size) * cell_size
            y = (i // grid_size) * cell_size
            collage.paste(img, (x, y))

        return collage

    st.title("Image Collage Maker with Custom Background")

    st.write("Upload images and create a collage with a custom background.")

    num_images_option = st.selectbox("Select the number of images for the collage:", [4, 9])
    uploaded_files = st.file_uploader("Upload your images", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")

    if len(uploaded_files) < num_images_option:
        st.warning(f"Please upload {num_images_option} images.")
        return

    # Read uploaded images
    images = []
    for file in uploaded_files[:num_images_option]:
        image = Image.open(file)
        images.append(image)

    # Create and display the collage
    if st.button("Create Collage"):
        collage = create_collage(images, num_images_option)
        if collage:
            st.image(collage, caption="Collage", use_column_width=True)

            # Provide a download button for the collage
            buffered = io.BytesIO()
            collage.save(buffered, format="JPEG")
            st.download_button(label="Download Collage", data=buffered.getvalue(), file_name="collage.jpg", mime="image/jpeg")

