import numpy as np

def bilinear_interpolation(image, new_width, new_height):
    """
    Perform bilinear interpolation to resize an image.

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
            x = i * row_ratio  # Calculate the corresponding pixel in the original image (x-coordinate)
            y = j * col_ratio  # Calculate the corresponding pixel in the original image (y-coordinate)

            x1 = int(np.floor(x))  # Get the integer part of the x-coordinate
            x2 = min(x1 + 1, height - 1)  # Get the next integer value for the x-coordinate, ensuring it's within bounds
            y1 = int(np.floor(y))  # Get the integer part of the y-coordinate
            y2 = min(y1 + 1, width - 1)  # Get the next integer value for the y-coordinate, ensuring it's within bounds
            
            a = x - x1  # Calculate the horizontal distance from x1
            b = y - y1  # Calculate the vertical distance from y1
            
            # Loop through each color channel (for RGB images)
            for c in range(channels):
                # Calculate the new pixel value using bilinear interpolation formula
                result[i, j, c] = (1 - a) * (1 - b) * image[x1, y1, c] + \
                                  a * (1 - b) * image[x2, y1, c] + \
                                  (1 - a) * b * image[x1, y2, c] + \
                                  a * b * image[x2, y2, c]

    return result  # Return the resized image


def resize_image_bilinear(image, new_width, new_height):
    """
    Resize an image using bilinear interpolation.

    Args:
        image (numpy.ndarray): The input image to be resized.
        new_width (int): The desired width of the output image.
        new_height (int): The desired height of the output image.

    Returns:
        numpy.ndarray: The resized image.
    """
    # Perform bilinear interpolation on the input image
    resized_image = bilinear_interpolation(image, new_width, new_height)
    
    return resized_image
