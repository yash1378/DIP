import numpy as np
import cv2

from processing import image_utils


def gaussian_kernel(size, sigma):
    """
    Generate a Gaussian kernel.

    Args:
        size (int): Size of the kernel (must be odd).
        sigma (float): Standard deviation of the Gaussian.

    Returns:
        numpy.ndarray: Gaussian kernel.
    """
    ax = np.linspace(-(size // 2), size // 2, size)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    return kernel / np.sum(kernel)

def gaussian_blur(image, kernel_size, sigma):
    """
    Apply Gaussian blur to an image.

    Args:
        image (numpy.ndarray): Grayscale input image.
        kernel_size (int): Size of the Gaussian kernel (must be odd).
        sigma (float): Standard deviation of the Gaussian.

    Returns:
        numpy.ndarray: Blurred image.
    """
    kernel = gaussian_kernel(kernel_size, sigma)
    padded_image = np.pad(image, kernel_size // 2, mode='edge')
    output_image = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # Convolution
            neighborhood = padded_image[i:i + kernel_size, j:j + kernel_size]
            output_image[i, j] = np.sum(neighborhood * kernel)
    
    return output_image.astype(np.uint8)


def gaussian_blur_color(image, kernel_size=7, sigma=100.0):
    """
    Apply Gaussian blur to each channel in a colored image.

    Args:
        image (numpy.ndarray): RGB input image.
        kernel_size (int): Size of the Gaussian kernel (must be odd).
        sigma (float): Standard deviation of the Gaussian.

    Returns:
        numpy.ndarray: Blurred color image.
    """
    # Split the image into R, G, B channels
    r, g, b = cv2.split(image)
    
    # Apply Gaussian blur to each channel
    r_blurred = gaussian_blur(r, kernel_size, sigma)
    g_blurred = gaussian_blur(g, kernel_size, sigma)
    b_blurred = gaussian_blur(b, kernel_size, sigma)
    
    # Merge the channels back
    return cv2.merge((r_blurred, g_blurred, b_blurred))

image_path = "./robot.jpg" 
original_image = image_utils.load_image(image_path)
blurred_image = gaussian_blur_color(original_image)

if __name__ == "__main__":
    image_utils.display_images([blurred_image], ["Gaussian Blurred image"])

