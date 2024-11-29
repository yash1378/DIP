import numpy as np
import cv2
# from processing import image_utils
# from processing import iterativebackprojection

# image_path = "./robot.jpg"
# original_image = image_utils.load_image(image_path)
# new_height, new_width = 1000,1000
# super_resolved_image = iterativebackprojection.iterative_back_projection(original_image,new_width,new_height)

#contrast
def calculate_contrast(image):
    min_val = np.min(image)
    max_val = np.max(image)
    return (max_val - min_val) / (max_val + min_val)

# contrast_img1 = calculate_contrast(original_image)
# contrast_img2 = calculate_contrast(super_resolved_image)
# print(f"Image 1 Contrast: {contrast_img1}, Image 2 Contrast: {contrast_img2}")