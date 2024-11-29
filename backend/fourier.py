import numpy as np
from nearest_neighbour_interpolation import nearest_neighbour_interpolation

def fourier_transform_super_resolution(image, new_width, new_height, radius=300, amp_factor=1.3):
    """
    Perform super-resolution using Fourier Transform.

    Args:
        image (numpy.ndarray): The input low-resolution image.
        new_width (int): The desired width of the output image.
        new_height (int): The desired height of the output image.
        radius (int): Radius of the low-frequency enhancement area (default is 300).
        amp_factor (float): Amplification factor for the low-frequency components (default is 1.3).

    Returns:
        numpy.ndarray: The high-resolution image.
    """
    # Convert the image to float and normalize to [0, 1]
    image_float = image.astype(np.float32) / 255.0

    # Perform Fourier Transform and shift zero frequency to center
    f_transform = np.fft.fft2(image_float)
    f_transform_shifted = np.fft.fftshift(f_transform)

    # Create a mask to amplify low-frequency components
    rows, cols = image.shape[:2]
    crow, ccol = rows // 2, cols // 2  # Center of the image
    mask = np.ones((rows, cols), np.float32)  # Initialize mask with ones
    
    # Create a circular region for low-frequency components in the mask
    y, x = np.ogrid[:rows, :cols]
    distance_from_center = (x - ccol)**2 + (y - crow)**2
    mask[distance_from_center <= radius**2] = amp_factor  # Amplify frequencies inside the circle

    # Apply the mask to the frequency components
    mask_expanded = mask[:, :, np.newaxis]  # Expand mask dimensions to match the frequency transform shape
    f_transform_shifted_masked = f_transform_shifted * mask_expanded

    # Perform inverse Fourier Transform
    f_transform_ishifted = np.fft.ifftshift(f_transform_shifted_masked)
    image_high_res = np.fft.ifft2(f_transform_ishifted)

    # Get the real part and normalize back to [0, 255]
    image_high_res = np.abs(image_high_res) * 255.0
    image_high_res = np.clip(image_high_res, 0, 255).astype(np.uint8)

    # Resize the high-resolution image to the desired dimensions
    high_res_image = nearest_neighbour_interpolation(image_high_res, new_width, new_height)

    return high_res_image