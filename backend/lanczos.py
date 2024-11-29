import numpy as np
import cv2

def lanczos_resample(image_path, new_width, new_height, a=3):
    """
    Load an image, perform Lanczos resampling, and return the resized image.
    
    Args:
        image_path (str): Path to the image to be loaded.
        new_width (int): Desired width of the output image.
        new_height (int): Desired height of the output image.
        a (int): Lobe size for Lanczos filter (default is 3).
        
    Returns:
        numpy.ndarray: Resized image.
    """
    
    # Load the image
    image = cv2.imread(image_path)  # Read the image
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB format
    
    # Perform Lanczos Resampling
    height, width, channels = image_rgb.shape
    result = np.zeros((new_height, new_width, channels), dtype=image_rgb.dtype)

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
                        pixel_value += weight * image_rgb[m, n]
                        total_weight += weight

            # Normalize the pixel value by the total weight to prevent brightness changes
            if total_weight > 0:
                result[i, j] = np.clip(pixel_value / total_weight, 0, 255)

    return result.astype(np.uint8)


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
        return np.sinc(x) * np.sinc(x / a)
    return 0.0
