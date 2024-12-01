import torch
from RRDBNet_arch import RRDBNet  # Import RRDBNet from the architecture file
import cv2
import numpy as np
from image_utils import display_images

def load_esrgan_model(weights_path):
    """
    Load ESRGAN model using predefined RRDB architecture.

    Args:
        weights_path (str): Path to the weights file.

    Returns:
        torch.nn.Module: Loaded ESRGAN model in evaluation mode.
    """
    # Define the ESRGAN RRDB architecture from the RRDBNet_arch.py
    model = RRDBNet(in_nc=3, out_nc=3, nf=64, nb=23, gc=32)
    
    # Load the pretrained weights into the model
    state_dict = torch.load(weights_path, map_location=torch.device('cpu'), weights_only=True)  # Adjust device if using GPU
    model.load_state_dict(state_dict, strict=True)  # Make sure the weights match the architecture
    model.eval()  # Set to evaluation mode
    
    return model

def preprocess_image(image_path):
    """
    Preprocess the image for the ESRGAN model.

    Args:
        image_path (str): Path to the input low-resolution image.

    Returns:
        torch.Tensor: Preprocessed image tensor.
    """
    # Read image using OpenCV and convert to RGB
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Normalize and convert to tensor
    img = img.astype(np.float32) / 255.0
    img = torch.from_numpy(np.transpose(img, (2, 0, 1))).unsqueeze(0)  # NCHW format
    
    return img

def postprocess_image(tensor):
    """
    Convert the model output tensor to a displayable image.

    Args:
        tensor (torch.Tensor): Output tensor from the ESRGAN model.

    Returns:
        numpy.ndarray: Postprocessed image as a numpy array.
    """
    img = tensor.squeeze(0).clamp_(0, 1).permute(1, 2, 0).numpy()  # HWC format
    img = (img * 255.0).astype(np.uint8)  # Convert to uint8
    return img

def super_resolve_image(model, lr_image):
    """
    Generate a super-resolved image using the ESRGAN model.

    Args:
        model (torch.nn.Module): Preloaded ESRGAN model.
        lr_image (torch.Tensor): Low-resolution input image tensor.

    Returns:
        numpy.ndarray: Super-resolved image as a numpy array.
    """
    with torch.no_grad():
        sr_tensor = model(lr_image)  # Super-resolve the image
    return postprocess_image(sr_tensor)

if __name__ == "__main__":
    weights_path = "RRDB_ESRGAN_x4.pth"  
    lr_image_path = "baboon.png"  

    # Load the model
    model = load_esrgan_model(weights_path)

    # Preprocess the low-resolution image
    lr_image = preprocess_image(lr_image_path)

    # Generate the super-resolved image
    sr_image = super_resolve_image(model, lr_image)

    # Display super resolved images
    display_images([sr_image],["super resolved image"])
