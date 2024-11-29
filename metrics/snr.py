import numpy as np
import cv2
from processing import image_utils
from processing import iterativebackprojection

image_path = "./robot.jpg"
original_image = image_utils.load_image(image_path)
new_height, new_width = 1000,1000
super_resolved_image = iterativebackprojection.iterative_back_projection(original_image,new_width,new_height)

#SNR
def calculate_snr(image):
    """
    Calculate the Signal-to-Noise Ratio (SNR) of an image.
    
    Parameters:
        image (numpy.ndarray): Input image in grayscale or color.
    
    Returns:
        float: SNR value.
    """
    # Convert image to grayscale if it is colored
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Compute the mean signal
    mean_signal = np.mean(image)
    
    # Compute the standard deviation of noise
    noise = image - mean_signal
    std_noise = np.std(noise)
    
    # Avoid division by zero
    if std_noise == 0:
        return float('inf')
    
    # Compute SNR
    snr = 20 * np.log10(mean_signal / std_noise)
    return snr

# Calculate SNR
snr_value_img1 = calculate_snr(original_image)
snr_value_img2 = calculate_snr(super_resolved_image)
print(f"SNR for image1: {snr_value_img1:.2f} dB, SNR for image2: {snr_value_img2:.2f} dB ")