import numpy as np
import cv2

from processing import image_utils

def saturation_adjust_color(image, saturation_scale=1.5):
    # Convert to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    H, S, V = cv2.split(hsv_image)

    # Adjust saturation
    S = np.clip(S * saturation_scale, 0, 255).astype(np.uint8)

    # Merge back and convert to BGR
    hsv_adjusted = cv2.merge((H, S, V))
    return cv2.cvtColor(hsv_adjusted, cv2.COLOR_HSV2RGB)

image_path = "./robot.jpg"  
original_image = image_utils.load_image(image_path)
enhanced_image = saturation_adjust_color(original_image)

if __name__ == "__main__":
    image_utils.display_images([enhanced_image], ["Enhanced image"])