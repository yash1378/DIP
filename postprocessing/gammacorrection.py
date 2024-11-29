import numpy as np
import cv2

from processing import image_utils

def gamma_correction(image, gamma):
    """
    Apply gamma correction to an image.

    Args:
        image (numpy.ndarray): Input image (grayscale or color).
        gamma (float): Gamma value. Values < 1 brighten the image, and values > 1 darken it.

    Returns:
        numpy.ndarray: Gamma-corrected image.
    """
    # Normalize the image to range [0, 1]
    normalized_image = image / 255.0

    # Apply the gamma correction formula: I' = I^gamma
    corrected_image = np.power(normalized_image, gamma)

    # Scale back to range [0, 255] and convert to uint8
    corrected_image = (corrected_image * 255).astype(np.uint8)

    return corrected_image


image_path = "./robot.jpg"  
original_image = image_utils.load_image(image_path)
gammacorrected_image = gamma_correction(original_image,0.5)

if __name__ == "__main__":
    image_utils.display_images([gammacorrected_image], ["Gamma corrected image"])

