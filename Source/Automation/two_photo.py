import cv2
from PIL import Image
import numpy as np

def capture_images():
    """Captures an image from the webcam.

    Returns:
        numpy.ndarray: The captured image as a NumPy array.
    """

    # Initialize the camera
    cap = cv2.VideoCapture(0)

    # Capture the image
    ret, frame = cap.read()

    # Release the camera
    cap.release()

    return frame

def merge_images(image1, image2, output_path):
    """Merges two images and saves the result.

    Args:
        image1 (numpy.ndarray): The first image.
        image2 (numpy.ndarray): The second image.
        output_path (str): The path to save the merged image.
    """

    # Convert OpenCV images to PIL images
    img1 = Image.fromarray(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
    img2 = Image.fromarray(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))

    # Resize second image to fit within the top-left corner of the first image
    width, height = img1.size
    img2 = img2.resize((width // 4, height // 4))  # Adjust the scaling as needed

    # Paste the second image onto the first image
    img1.paste(img2, (0, 0))  # Top-left corner

    Image._show(img1)

    # Save the result
    img1.save(output_path)

def capture_and_merge_interactive():
    """Captures two images interactively, displays them for review, and saves them on confirmation.

    Press 'q' to quit or any other key to capture the next image.
    Press 's' to save the merged image after capturing both images.
    """

    # Capture the first image
    image1 = capture_images()

    # Display the first image
    cv2.imshow("Image 1", image1)

    # Capture the second image or exit
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("s"):
            # Capture the second image if not already captured
            if image2 is None:
                image2 = capture_images()
                cv2.imshow("Image 2", image2)
            else:
                # Merge and save images
                output_path = rf"C:\Users\dragon389\Desktop\General\Source\Automation\Outputs\images\merged_image_{np.random.randint(1, 1000)}.jpg"
                merge_images(image1, image2, output_path)
                print(f"Merged image saved to: {output_path}")
                break
        else:
            # Capture the second image
            image2 = capture_images()
            cv2.imshow("Image 2", image2)

    # Close all windows
    cv2.destroyAllWindows()

