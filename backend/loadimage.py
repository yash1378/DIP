import cv2

def load_image(image):
    """
    Load an image from the specified path and convert it to RGB format.
    
    Args:
        image_path (str): The path to the image file.

    Returns:
        numpy.ndarray: The loaded RGB image.
    """
    # image = cv2.imread(image_path)  # Read the image
    if image is None:
        raise FileNotFoundError(f"Image not found")  # Raise error if the image is not found
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB format