import numpy as np
from image_utils import load_image, display_images, draw_pixel_trace
from nearestneighbour import nearest_neighbour_interpolation

# Load the low-resolution image
image_path = "./robot.jpg"  # Replace with your image path
lr_image = load_image(image_path)  # Use the load_image function

# Example of displaying the loaded image
# display_images([lr_image], ["Low-Resolution Image"])

# # Example of drawing pixel traces
# traced_image = draw_pixel_trace(lr_image, pixel_size=5)  # Adjust pixel size as needed
# display_images([traced_image], ["Traced Image"])

# Fourier Transform Based SR
def fourier_transform_super_resolution(image, new_width, new_height, radius=300, amp_factor=1.3):
    """
    Perform super-resolution using Fourier Transform.

    Args:
        image (numpy.ndarray): The input low-resolution image.
        new_width (int): The desired width of the output image.
        new_height (int): The desired height of the output image.

    Returns:
        numpy.ndarray: The high-resolution image.
    """
    # Convert the image to float and normalize to [0, 1]
    image_float = image.astype(np.float32) / 255.0

    # Perform Fourier Transform
    f_transform = np.fft.fft2(image_float)
    f_transform_shifted = np.fft.fftshift(f_transform)  # Shift zero frequency component to center

    # Create a mask to enhance frequency components
    rows, cols = image.shape[:2]
    crow, ccol = rows // 2, cols // 2  # Center of the image
    mask = np.full((rows, cols), 1, np.float32)
    
    # Define a circular area in the mask to amplify low frequencies
    y, x = np.ogrid[:rows, :cols]
    distance_from_center = (x - ccol)**2 + (y - crow)**2
    mask[distance_from_center <= radius**2] = amp_factor  # Set inside circle to 1

    # Apply the mask to the shifted frequency domain
    # Expand mask dimensions to match the frequency transform shape
    mask_expanded = mask[:, :, np.newaxis]  # Add a new axis to make it (rows, cols, 1)

    # Apply mask to the shifted frequency domain
    f_transform_shifted_masked = f_transform_shifted * mask_expanded

    # Inverse shift and perform Inverse Fourier Transform
    f_transform_ishifted = np.fft.ifftshift(f_transform_shifted_masked)
    image_high_res = np.fft.ifft2(f_transform_ishifted)

    # Get the real part and normalize back to [0, 255]
    image_high_res = np.abs(image_high_res) * 255.0
    image_high_res = np.clip(image_high_res, 0, 255).astype(np.uint8)

    # Resize the image to the desired dimensions
    high_res_image = nearest_neighbour_interpolation(image_high_res, new_width, new_height)

    return high_res_image


# Example
# Set new dimensions for the output image
new_height, new_width = 750, 750  # Replace with your desired dimensions

# Note: Avoid keeping the amp_factor too high(1-1.5 is fine)
# Also keeping radius less will include less low frequency components
fft_image = fourier_transform_super_resolution(lr_image, new_width, new_height)
# Display results
if __name__ == "__main__":
    display_images([fft_image], ["Fourier Transform Super Resolution"])