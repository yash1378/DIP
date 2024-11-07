import numpy as np
import pywt
import cv2
from image_utils import load_image, display_images, draw_pixel_trace
from nearest_neighbour_interpolation import nearest_neighbour_interpolation

# Load the low-resolution image
image_path = "./robot.jpg"  # Replace with your image path
lr_image = load_image(image_path)  # Use the load_image function

# Example of displaying the loaded image
# display_images([lr_image], ["Low-Resolution Image"])

# Example of drawing pixel traces
# traced_image = draw_pixel_trace(lr_image, pixel_size=5)  # Adjust pixel size as needed
# display_images([traced_image], ["Traced Image"])

# Wavelet based SR
def wavelet_super_resolution_color(image, new_width, new_height):
    """
    Perform super-resolution on a color image using wavelet transforms.
    
    Args:
    - image (numpy.ndarray): Low-resolution color image of shape (height, width, 3).
    - new_width (int): Desired width of the output image.
    - new_height (int): Desired height of the output image.
    
    Returns:
    - numpy.ndarray: Super-resolved color image of shape (new_height, new_width, 3).
    """
    # Split the image into its RGB channels
    channels = cv2.split(image)
    
    # Initialize an empty list to hold the super-resolved channels
    super_resolved_channels = []
    
    for channel in channels:
        # Perform 2D Discrete Wavelet Transform
        cA, (cH, cV, cD) = pywt.dwt2(channel, 'haar')
        
        # Upscale the approximation coefficients using your nearest neighbor function
        cA_resized = nearest_neighbour_interpolation(cA, new_width, new_height)
        
        # Upscale the detail coefficients using your nearest neighbor function
        cH_resized = nearest_neighbour_interpolation(cH, new_width, new_height)
        cV_resized = nearest_neighbour_interpolation(cV, new_width, new_height)
        cD_resized = nearest_neighbour_interpolation(cD, new_width, new_height)
        
        # Reconstruct the image using the resized coefficients
        super_resolved_channel = pywt.idwt2((cA_resized, (cH_resized, cV_resized, cD_resized)), 'haar')
        
        # Clip values to the range [0, 255] and convert to uint8
        super_resolved_channel = np.clip(super_resolved_channel, 0, 255).astype(np.uint8)
        
        # Append the super-resolved channel to the list
        super_resolved_channels.append(super_resolved_channel)
    
    # Merge the super-resolved channels back into a single image
    super_resolved_image = cv2.merge(super_resolved_channels)
    
    return super_resolved_image


# Example
# Set new dimensions for the output image
new_height, new_width = 750, 750  # Replace with your desired dimensions

# Perform interpolations
wavelet_image = wavelet_super_resolution_color(lr_image, new_width, new_height)

# Display results
if __name__ == "__main__":
    display_images([wavelet_image], ["Wavelet based SR"])