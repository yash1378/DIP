import numpy as np
from image_utils import load_image, display_images, draw_pixel_trace
from nearestneighbour import nearest_neighbour_interpolation

# Load the low-resolution image
image_path = "./robot.jpg"  # Replace with your image path
lr_image = load_image(image_path)  # Use the load_image function

# Example of displaying the loaded image
# display_images([lr_image], ["Low-Resolution Image"])

# Example of drawing pixel traces
# traced_image = draw_pixel_trace(lr_image, pixel_size=5)  # Adjust pixel size as needed
# display_images([traced_image], ["Traced Image"])

# Total Variation
def total_variation_denoising(image, weight=10, iterations=1000):
    """
    Apply Total Variation Regularization for denoising an image.

    Args:
        image (numpy.ndarray): Input low-resolution image.
        weight (float): Weight for the total variation term.
        iterations (int): Number of iterations to perform.

    Returns:
        numpy.ndarray: Denoised image.
    """
    # Initialize the output image
    output = np.copy(image).astype(np.float32)

    # Gradient descent loop
    for _ in range(iterations):
        # Calculate gradients in x and y directions
        dx = np.roll(output, -1, axis=1) - output  # Horizontal gradient
        dy = np.roll(output, -1, axis=0) - output  # Vertical gradient

        # Compute the total variation (L2 norm of gradients)
        tv = np.sqrt(dx ** 2 + dy ** 2) + 1e-10  # Adding a small epsilon to prevent division by zero

        # Update the output image using the total variation regularization term
        output -= weight * (dx / tv + dy / tv)  # Update based on the gradients

        # Optional: Clip values to keep them in valid range [0, 255]
        output = np.clip(output, 0, 255)

    return output.astype(np.uint8)  # Return as uint8 image

def upscale_with_tv(image, new_width, new_height):
    """
    Upscale the image and apply Total Variation Regularization.

    Args:
        image (numpy.ndarray): Input low-resolution image.
        new_width (int): Desired width of the output image.
        new_height (int): Desired height of the output image.

    Returns:
        numpy.ndarray: Super-resolved image with total variation denoising.
    """
    # Step 1: Upscale the image using nearest neighbour interpolation
    upscaled_image = nearest_neighbour_interpolation(image, new_width, new_height)

    # Step 2: Apply Total Variation Regularization
    denoised_image = total_variation_denoising(upscaled_image, weight=0.1, iterations=100)

    return denoised_image


# Example
# Set new dimensions for the output image
new_height, new_width = 700, 700  # Replace with your desired dimensions

tv_image = upscale_with_tv(lr_image, new_width, new_height)

# Display results
if __name__ == "__main__":
    display_images([tv_image], ["Total Variation SR"])