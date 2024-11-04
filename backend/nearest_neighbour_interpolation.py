import numpy as np

def nearest_neighbour_interpolation(image, new_width, new_height):
    """
    Perform nearest-neighbor interpolation to resize an image.

    Args:
        image (numpy.ndarray): The input image.
        new_width (int): The desired width of the output image.
        new_height (int): The desired height of the output image.

    Returns:
        numpy.ndarray: The resized image.
    """
    height, width, channels = image.shape  # Get the original dimensions of the image
    result = np.zeros((new_height, new_width, channels), dtype=image.dtype)  # Create an empty output image

    # Calculate the ratio of original dimensions to new dimensions
    row_ratio = height / new_height  # Ratio for height
    col_ratio = width / new_width  # Ratio for width

    # Loop through each pixel in the new image
    for i in range(new_height):
        for j in range(new_width):
            # Calculate the nearest pixel coordinates in the original image
            nearest_x = int(i * row_ratio)  # Corresponding pixel's x-coordinate
            nearest_y = int(j * col_ratio)  # Corresponding pixel's y-coordinate
            
            # Ensure indices do not exceed original image bounds
            nearest_x = min(nearest_x, height - 1)
            nearest_y = min(nearest_y, width - 1)
            
            # Assign the color of the nearest pixel to the result image
            result[i, j] = image[nearest_x, nearest_y]

    return result  # Return the resized image
