import numpy as np

def cubic_weight(t):
    """
    Calculate the cubic weight based on the distance from the pixel center.

    Args:
        t (float): The distance from the pixel center.

    Returns:
        float: The weight for the cubic interpolation.
    """
    abs_t = abs(t)
    if abs_t <= 1:
        return (1.5 * abs_t**3) - (2.5 * abs_t**2) + 1
    elif abs_t <= 2:
        return (-0.5 * abs_t**3) + (2.5 * abs_t**2) - (4 * abs_t) + 2
    else:
        return 0

def bicubic_interpolation(image, new_width, new_height):
    """
    Perform bicubic interpolation to resize an image.

    Args:
        image (numpy.ndarray): The input image.
        new_width (int): The desired width of the output image.
        new_height (int): The desired height of the output image.

    Returns:
        numpy.ndarray: The resized image.
    """
    # if len(image.shape) == 2:  # Grayscale image
    #     image = np.expand_dims(image, axis=-1)  # Add a channel dimension
    height, width, channels = image.shape
    result = np.zeros((new_height, new_width, channels), dtype=image.dtype)

    row_ratio = height / new_height
    col_ratio = width / new_width

    for i in range(new_height):
        for j in range(new_width):
            x = i * row_ratio
            y = j * col_ratio

            x_int = int(np.floor(x))
            y_int = int(np.floor(y))
            x_frac = x - x_int
            y_frac = y - y_int

            for c in range(channels):
                pixel_value = 0

                for m in range(-1, 3):
                    for n in range(-1, 3):
                        xm = np.clip(x_int + m, 0, height - 1)
                        yn = np.clip(y_int + n, 0, width - 1)
                        
                        pixel_value += (
                            image[xm, yn, c]
                            * cubic_weight(m - x_frac)
                            * cubic_weight(n - y_frac)
                        )

                result[i, j, c] = np.clip(pixel_value, 0, 255)
                
    print(result)
    print(len(result))
    print(result.astype(np.uint8))
    return result.astype(np.uint8)