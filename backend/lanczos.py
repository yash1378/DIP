import numpy as np

# Load the low-resolution image
# image_path = "./robot.jpg"  # Replace with your image path
# lr_image = load_image(image_path)  # Use the load_image function

# Example of displaying the loaded image
# display_images([lr_image], ["Low-Resolution Image"])

# Example of drawing pixel traces
# traced_image = draw_pixel_trace(lr_image, pixel_size=5)  # Adjust pixel size as needed
# display_images([traced_image], ["Traced Image"])

# Lanczos Resampling
def sinc(x):
    """Return sinc(x) which is sin(πx) / (πx) but handles x=0 case."""
    return np.sinc(x / np.pi)

def lanczos_kernel(x, a):
    """
    Calculate the Lanczos kernel function for a given x and lobe size a.
    
    Args:
        x (float): Distance from the center pixel.
        a (int): Lobe size, which determines the range of the filter.
        
    Returns:
        float: Kernel value based on distance and lobe size.
    """
    if abs(x) < a:
        return sinc(x) * sinc(x / a)
    return 0.0

def lanczos_resample(image, new_width, new_height, a=3):
    """
    Perform Lanczos resampling to resize an image.
    
    Args:
        image (numpy.ndarray): The input image.
        new_width (int): Desired width of the output image.
        new_height (int): Desired height of the output image.
        a (int): Lobe size for Lanczos filter (common values are 2 or 3).
        a -> The parameter a affects the sharpness and smoothness of the result, with higher values providing sharper images but potentially introducing ringing artifacts.
        
    Returns:
        numpy.ndarray: Resized image.
    """
    height, width, channels = image.shape
    result = np.zeros((new_height, new_width, channels), dtype=image.dtype)

    # Scale ratios
    row_ratio = height / new_height
    col_ratio = width / new_width

    # Loop over each pixel in the output image
    for i in range(new_height):
        for j in range(new_width):
            # Map output pixel (i, j) to corresponding coordinates in input image
            src_x = i * row_ratio
            src_y = j * col_ratio

            # Nearest integer pixel in input image
            x_int = int(np.floor(src_x))
            y_int = int(np.floor(src_y))

            # Initialize pixel value for each color channel
            pixel_value = np.zeros(channels)

            # Sum weights and contributions for each channel
            total_weight = 0.0

            # Loop over nearby pixels in the input image within the lobe size
            for m in range(x_int - a + 1, x_int + a):
                for n in range(y_int - a + 1, y_int + a):
                    if 0 <= m < height and 0 <= n < width:
                        # Calculate distance from center in x and y directions
                        dx = src_x - m
                        dy = src_y - n
                        
                        # Compute the weight using the Lanczos kernel
                        weight = lanczos_kernel(dx, a) * lanczos_kernel(dy, a)
                        
                        # Accumulate the weighted pixel value
                        pixel_value += weight * image[m, n]
                        total_weight += weight

            # Normalize the pixel value by the total weight to prevent brightness changes
            if total_weight > 0:
                result[i, j] = np.clip(pixel_value / total_weight, 0, 255)

    return result.astype(np.uint8)


# # Example
# # Set new dimensions for the output image
# new_height, new_width = 500, 300  # Replace with your desired dimensions

# # Perform interpolations
# lanczos_image = lanczos_resample(lr_image, new_width, new_height)

# # Display results
# if __name__ == "__main__":
#     display_images([lanczos_image], ["Lanczos Resampling"])