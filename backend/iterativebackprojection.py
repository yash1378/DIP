import numpy as np
import cv2
from image_utils import load_image, display_images, draw_pixel_trace
from nearest_neighbour_interpolation import nearest_neighbour_interpolation

# Example of displaying the loaded image
# display_images([lr_image], ["Low-Resolution Image"])

# Example of drawing pixel traces
# traced_image = draw_pixel_trace(lr_image, pixel_size=5)  # Adjust pixel size as needed
# display_images([traced_image], ["Traced Image"])

# Iterative Back Projection
def upsample_image(image, new_width, new_height):
    """
    Upsample the image using nearest neighbor interpolation.

    Args:
        image (numpy.ndarray): Input image.
        new_width (int): Desired width for the upsampled image.
        new_height (int): Desired height for the upsampled image.

    Returns:
        numpy.ndarray: Upsampled image.
    """
    nearest_upsampled = nearest_neighbour_interpolation(image, new_width, new_height)
    return nearest_upsampled

def project_image(hr_image, lr_width, lr_height):
    """
    Project the high-resolution image to low-resolution by downsampling.

    Args:
        hr_image (numpy.ndarray): High-resolution image.
        lr_width (int): Width for the downsampled image.
        lr_height (int): Height for the downsampled image.

    Returns:
        numpy.ndarray: Downsampled low-resolution image.
    """
    # bilinear_downsampled = bilinear_interpolation(hr_image, new_width, new_height)
    # return bilinear_downsampled
    return cv2.resize(hr_image, (lr_width, lr_height), interpolation=cv2.INTER_LINEAR)

def iterative_back_projection(lr_image, new_width, new_height, iterations=10):
    """
    Perform iterative back projection for super-resolution.

    Args:
        lr_image (numpy.ndarray): Low-resolution input image.
        new_width (int): Desired width for the output super-resolved image.
        new_height (int): Desired height for the output super-resolved image.
        iterations (int): Number of iterations to perform.

    Returns:
        numpy.ndarray: Super-resolved image.
    """
    # Step 1: Get the original dimensions of the low-resolution image
    lr_height, lr_width = lr_image.shape[:2]

    # Step 2: Initialize with upsampled low-resolution image
    hr_image = upsample_image(lr_image, new_width, new_height)

    # Iterate for the specified number of times
    for _ in range(iterations):
        # Step 3: Project the current HR image to the original LR dimensions
        lr_projected = project_image(hr_image, lr_width, lr_height)

        # Step 4: Calculate the error (difference) between LR image and projected HR image
        error = lr_image.astype(np.float32) - lr_projected.astype(np.float32)

        # Step 5: Back-project the error onto the HR image
        # Upsample the error to the size of the HR image
        error_upsampled = upsample_image(error, new_width, new_height)

        # Step 6: Update the HR image
        # Convert hr_image to float32 for addition
        hr_image = hr_image.astype(np.float32) + error_upsampled

        # Optional: Clip the values to keep them in valid range [0, 255]
        hr_image = np.clip(hr_image, 0, 255)

    return hr_image.astype(np.uint8)  # Return as uint8 image