import numpy as np
from image_utils import load_image, display_images, draw_pixel_trace

# Load the low-resolution image
image_path = "./robot.jpg"  # Replace with your image path
lr_image = load_image(image_path)  # Use the load_image function

# Example of displaying the loaded image
# display_images([lr_image], ["Low-Resolution Image"])

# # Example of drawing pixel traces
# traced_image = draw_pixel_trace(lr_image, pixel_size=5)  # Adjust pixel size as needed
# display_images([traced_image], ["Traced Image"])

# Nearest-Neighbor Interpolation
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
            
            # Assign the color of the nearest pixel to the result image
            result[i, j] = image[nearest_x, nearest_y]

    return result  # Return the resized image


# Example
# Set new dimensions for the output image
new_height, new_width = 500, 300  # Replace with your desired dimensions

# Perform interpolations
nearest_neighbour_image = nearest_neighbour_interpolation(lr_image, new_width, new_height)

# Display results
if __name__ == "__main__":
    display_images([nearest_neighbour_image], ["Nearest Neighbour"])