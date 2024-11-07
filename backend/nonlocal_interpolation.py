import numpy as np
from image_utils import load_image, display_images, draw_pixel_trace
from nearest_neighbour_interpolation import nearest_neighbour_interpolation

def compute_weighted_average(patch, target_patch, h):
    """
    Compute the weighted average of a pixel based on patch similarity.
    The weights are determined by the similarity between the patches.
    
    Args:
        patch (numpy.ndarray): A patch around the current pixel.
        target_patch (numpy.ndarray): The target patch to compare similarity.
        h (float): The filtering parameter controlling the decay of weights.
        
    Returns:
        float: Weight based on similarity.
    """
    # Calculate the L2 distance between the patches (Euclidean distance)
    diff = patch - target_patch
    dist2 = np.sum(diff ** 2)

    # Compute the weight based on Gaussian function
    weight = np.exp(-np.clip(dist2 / (h ** 2), -100, 0))
    return weight

def non_local_means_super_resolution(image, new_width, new_height, h=10, template_window_size=3, search_window_size=11):
    """
    Apply Non-Local Means filtering to an upscaled version of the input image for super-resolution.
    
    Args:
        image (numpy.ndarray): Input low-resolution image.
        new_width (int): Target width of the super-resolved image.
        new_height (int): Target height of the super-resolved image.
        h (float): Parameter controlling filter strength (higher = stronger denoising).
        template_window_size (int): Size of the window for template matching.
        search_window_size (int): Size of the window to search for similar patches.
        
    Returns:
        numpy.ndarray: Super-resolved image.
    """
    # Step 1: Upscale the image using nearest neighbor interpolation
    upscaled_image = nearest_neighbour_interpolation(image, new_width, new_height)

    # Pad the image to handle border pixels
    padded_image = np.pad(upscaled_image, ((search_window_size//2, search_window_size//2), 
                                           (search_window_size//2, search_window_size//2), (0, 0)), 'reflect')

    # Initialize the output image
    filtered_image = np.zeros_like(upscaled_image, dtype=np.float64)

    # Iterate over each pixel in the upscaled image
    for i in range(upscaled_image.shape[0]):
        for j in range(upscaled_image.shape[1]):
            # Define the template (target) patch centered at the pixel (i, j)
            target_patch = padded_image[i:i + template_window_size, j:j + template_window_size]

            # Define search window around the current pixel (i, j)
            search_region = padded_image[i:i + search_window_size, j:j + search_window_size]

            # Variables to accumulate weights and pixel values
            weighted_sum = np.zeros(3)
            total_weight = 0.0

            # Slide over the search window to compute weights for each patch
            for k in range(search_window_size - template_window_size + 1):
                for l in range(search_window_size - template_window_size + 1):
                    # Get the neighboring patch
                    neighbor_patch = search_region[k:k + template_window_size, l:l + template_window_size]

                    # Compute weight based on similarity
                    weight = compute_weighted_average(target_patch, neighbor_patch, h)

                    # Accumulate weighted sum for each color channel
                    weighted_sum += weight * search_region[k + template_window_size // 2, l + template_window_size // 2]
                    total_weight += weight
            
            # Avoid division by zero
            if total_weight == 0:
                filtered_image[i, j] = image[i, j]
            else:
                filtered_image[i, j] = weighted_sum / total_weight

            # Normalize by total weight to get the final pixel value
            filtered_image[i, j] = weighted_sum / total_weight

    # Clip values to valid range and convert to uint8
    filtered_image = np.clip(filtered_image, 0, 255).astype(np.uint8)
    return filtered_image
