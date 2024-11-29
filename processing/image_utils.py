import numpy as np
import cv2
import matplotlib.pyplot as plt

def load_image(image_path):
    """
    Load an image from the specified path and convert it to RGB format.
    
    Args:
        image_path (str): The path to the image file.

    Returns:
        numpy.ndarray: The loaded RGB image.
    """
    image = cv2.imread(image_path)  # Read the image
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")  # Raise error if the image is not found
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB format

def display_images(images, titles):
    """
    Display a list of images with their corresponding titles.
    
    Args:
        images (list of numpy.ndarray): List of images to display.
        titles (list of str): Corresponding titles for the images.
    """
    for img, title in zip(images, titles):
        plt.imshow(img)
        plt.title(title)
        plt.axis('off')

        # Create a callback to handle key press events
        def on_key(event):
            if event.key == 'q':
                plt.close()  # Close the current figure window

        plt.gcf().canvas.mpl_connect('key_press_event', on_key)  # Connect the key press event
        plt.show()  # Show the image

def draw_pixel_trace(image, pixel_size=1):
    """
    Draw rectangles around each pixel in the image.
    
    Args:
        image (numpy.ndarray): The input image.
        pixel_size (int): The size of the pixels to trace.

    Returns:
        numpy.ndarray: The traced image with pixel outlines.
    """
    traced_image = image.copy()
    # Draw rectangles for each pixel
    for i in range(image.shape[0]):  # height
        for j in range(image.shape[1]):  # width
            # Calculate the top-left and bottom-right corners of the rectangle
            top_left = (j * pixel_size, i * pixel_size)
            bottom_right = ((j + 1) * pixel_size, (i + 1) * pixel_size)
            # Draw a rectangle for each pixel
            cv2.rectangle(traced_image, top_left, bottom_right, (255, 0, 0), thickness=1)  # Red rectangles
    return traced_image
