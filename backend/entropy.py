import numpy as np
import cv2
# from processing import image_utils
# from processing import iterativebackprojection

# image_path = "./robot.jpg"
# original_image = image_utils.load_image(image_path)
# new_height, new_width = 1000,1000
# super_resolved_image = iterativebackprojection.iterative_back_projection(original_image,new_width,new_height)

#entropy
from skimage.measure import shannon_entropy

def calculate_entropy(image):
    return shannon_entropy(image)

# entropy_img1 = calculate_entropy(original_image)
# entropy_img2 = calculate_entropy(super_resolved_image)
# print(f"Image 1 Entropy: {entropy_img1}, Image 2 Entropy: {entropy_img2}")