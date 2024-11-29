import numpy as np
import cv2


def sobel_edge_detection(image):
    """
    Detect edges using the Sobel operator.

    Args:
        image (numpy.ndarray): Grayscale input image.

    Returns:
        numpy.ndarray: Edge-detected image.
    """
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1],
                        [ 0,  0,  0],
                        [ 1,  2,  1]])

    padded_image = np.pad(image, 1, mode='edge')
    grad_magnitude = np.zeros_like(image, dtype=np.float32)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            neighborhood = padded_image[i:i + 3, j:j + 3]
            gx = np.sum(neighborhood * sobel_x)
            gy = np.sum(neighborhood * sobel_y)
            grad_magnitude[i, j] = np.sqrt(gx**2 + gy**2)
    
    return np.clip(grad_magnitude, 0, 255).astype(np.uint8)


def sobel_edge_detection_color(image):
    """
    Detect edges in each channel of a colored image using the Sobel operator.

    Args:
        image (numpy.ndarray): RGB input image.

    Returns:
        numpy.ndarray: Edge-detected color image.
    """
    # Split the image into R, G, B channels
    r, g, b = cv2.split(image)
    
    # Apply Sobel edge detection to each channel
    r_edges = sobel_edge_detection(r)
    g_edges = sobel_edge_detection(g)
    b_edges = sobel_edge_detection(b)
    
    # Merge the channels back
    return cv2.merge((r_edges, g_edges, b_edges))

# image_path = "./robot.jpg"  
# original_image = image_utils.load_image(image_path)
# edgedetected_image = sobel_edge_detection_color(original_image)

# if __name__ == "__main__":
#     image_utils.display_images([edgedetected_image], ["Edge detection"])