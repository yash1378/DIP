# iterative_back_projection.py

import numpy as np
import cv2
from nearest_neighbour_interpolation import nearest_neighbour_interpolation

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
    # Get the original dimensions of the low-resolution image
    lr_height, lr_width = lr_image.shape[:2]

    # Initialize with upsampled low-resolution image
    hr_image = upsample_image(lr_image, new_width, new_height)

    # Iterate for the specified number of times
    for _ in range(iterations):
        # Project the current HR image to the original LR dimensions
        lr_projected = project_image(hr_image, lr_width, lr_height)

        # Calculate the error (difference) between LR image and projected HR image
        error = lr_image.astype(np.float32) - lr_projected.astype(np.float32)

        # Back-project the error onto the HR image
        # Upsample the error to the size of the HR image
        error_upsampled = upsample_image(error, new_width, new_height)

        # Update the HR image
        hr_image = hr_image.astype(np.float32) + error_upsampled

        # Clip values to keep them in valid range [0, 255]
        hr_image = np.clip(hr_image, 0, 255)

    return hr_image.astype(np.uint8)  # Return as uint8 image
