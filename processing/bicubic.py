import numpy as np
from .image_utils import load_image, display_images, draw_pixel_trace

# Load the low-resolution image
image_path = "./robot.jpg"  # Replace with your image path
lr_image = load_image(image_path)  # Use the load_image function

# Example of displaying the loaded image
# display_images([lr_image], ["Low-Resolution Image"])

# Example of drawing pixel traces
# traced_image = draw_pixel_trace(lr_image, pixel_size=5)  # Adjust pixel size as needed
# display_images([traced_image], ["Traced Image"])

# Bicubic Interpolation (Interpolation algo)
def cubic_weight(t):
    """
    Calculate the cubic weight based on the distance from the pixel center.

    Args:
        t (float): The distance from the pixel center.

    Returns:
        float: The weight for the cubic interpolation.
    """
    abs_t = abs(t)  # Get the absolute value of t
    if abs_t <= 1:  # If t is within the range [-1, 1]
        return (1.5 * abs_t**3) - (2.5 * abs_t**2) + 1  # Calculate weight using the first cubic equation
    elif abs_t <= 2:  # If t is within the range (1, 2]
        return (-0.5 * abs_t**3) + (2.5 * abs_t**2) - (4 * abs_t) + 2  # Calculate weight using the second cubic equation
    else:
        return 0  # Outside the range, weight is 0

def bicubic_interpolation(image, new_width, new_height):
    """
    Perform bicubic interpolation to resize an image.

    Args:
        image (numpy.ndarray): The input image.
        new_width (int): The desired width of the output image.
        new_height (int): The desired height of the output image.

    Returns:
        numpy.ndarray: The resized image.
    """
    height, width, channels = image.shape  # Get the original dimensions of the image
    result = np.zeros((new_height, new_width, channels), dtype=image.dtype)  # Create an empty output image

    row_ratio = height / new_height  # Calculate the ratio of original height to new height
    col_ratio = width / new_width  # Calculate the ratio of original width to new width

    # Loop through each pixel in the new image
    for i in range(new_height):
        for j in range(new_width):
            x = i * row_ratio  # Calculate the corresponding pixel in the original image (x-coordinate)
            y = j * col_ratio  # Calculate the corresponding pixel in the original image (y-coordinate)

            x_int = int(np.floor(x))  # Get the integer part of x
            y_int = int(np.floor(y))  # Get the integer part of y
            x_frac = x - x_int  # Calculate the fractional part of x
            y_frac = y - y_int  # Calculate the fractional part of y

            # Loop through each channel (for RGB images)
            for c in range(channels):
                pixel_value = 0  # Initialize the pixel value for the new pixel

                # Loop through the 4x4 neighborhood around the pixel
                for m in range(-1, 3):  # m ranges from -1 to 2
                    for n in range(-1, 3):  # n ranges from -1 to 2
                        # Clip the pixel index to ensure it stays within the image boundaries
                        xm = np.clip(x_int + m, 0, height - 1)  # Get the x index of the pixel
                        yn = np.clip(y_int + n, 0, width - 1)  # Get the y index of the pixel
                        
                        # Update the pixel value using the cubic weights
                        pixel_value += image[xm, yn, c] * cubic_weight(m - x_frac) * cubic_weight(n - y_frac)
                
                result[i, j, c] = np.clip(pixel_value, 0, 255)  # Store the computed pixel value in the result image

    return result.astype(np.uint8)  # Return the result as an unsigned 8-bit integer image


# Example
# Set new dimensions for the output image
new_height, new_width = 500, 300  # Replace with your desired dimensions

# Perform interpolations
bicubic_image = bicubic_interpolation(lr_image, new_width, new_height)

# Display results
if __name__ == "__main__":
    display_images([bicubic_image], ["Bicubic"])