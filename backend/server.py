from flask import Flask, jsonify, request, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
from io import BytesIO
import numpy as np
from nearest_neighbour_interpolation import nearest_neighbour_interpolation  # Adjust based on your directory structure
from bicubic_interpolation import bicubic_interpolation
from bilinear import bilinear_interpolation
from fourier import fourier_transform_super_resolution
from iterativebackprojection import iterative_back_projection
from lanczos import lanczos_resample
from nonlocal_interpolation import non_local_means_super_resolution
from totalvariation import total_variation_denoising
from wavelet import wavelet_super_resolution_color

import base64
import os
import sys
from PIL import Image
import io

# Add the root directory to sys.path to access 'processing' as a sibling directory to 'backend'
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)
# Define a directory to save processed images
PROCESSED_IMAGE_DIR = 'processed_images'

# Ensure the directory exists
os.makedirs(PROCESSED_IMAGE_DIR, exist_ok=True)

# from processing import bicubic

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/api/list_super_resolution_methods')
def get_methods():
    methods = [
        {
            "id": 1,
            "name": "Bicubic Interpolation",
            "description": "A high-quality resampling technique using cubic splines.",
            "complexity": "O(n^2)",
            "category": "Image Processing",
            "performance": 0,
            "tags": ["interpolation", "cubic", "resampling"]
        },
        {
            "id": 2,
            "name": "SRCNN",
            "description": "Super-Resolution Convolutional Neural Network for image upscaling.",
            "complexity": "O(n^2)",
            "category": "Image Processing",
            "performance": 0,
            "tags": ["deep learning", "CNN", "super resolution"]
        },
        {
            "id": 3,
            "name": "ESRGAN",
            "description": "Enhanced Super-Resolution Generative Adversarial Network.",
            "complexity": "O(n^2)",
            "category": "Image Processing",
            "performance": 0,
            "tags": ["GAN", "deep learning", "super resolution"]
        }
    ]
    return jsonify(methods)

@app.route('/api/list_post_processing_methods')
def get_processing_steps():
    processing_steps = [
        {
            "id": "ps1",
            "name": "Noise Reduction",
            "description": "Reduces random variation of brightness or color information in the image.",
            "impact": "High",
            "category": "Post Processing",
            "timeRequired": "0",
            "features": ["Smoothing", "Detail preservation"]
        },
        {
            "id": "ps2",
            "name": "Color Correction",
            "description": "Adjusts the color balance of the image to appear more natural or vibrant.",
            "impact": "Medium",
            "category": "Post Processing",
            "timeRequired": "0",
            "features": ["White balance", "Saturation adjustment"]
        },
        {
            "id": "ps3",
            "name": "Sharpening",
            "description": "Enhances edge contrast to make the image appear more defined.",
            "impact": "Medium",
            "category": "Post Processing",
            "timeRequired": "0",
            "features": ["Edge enhancement", "Detail accentuation"]
        }
    ]
    return jsonify(processing_steps)

@app.route('/api/apply-algorithm', methods=['POST'])
def apply_algorithm():
    data = request.get_json()
    
    if not data or 'imageData' not in data or 'algoId' not in data:
        return jsonify({"error": "No image file or algorithm ID provided"}), 400

    image_data = data['imageData']
    algorithm_id = data['algoId']

    # Decode base64 image
    header, encoded = image_data.split(',', 1)
    image_bytes = base64.b64decode(encoded)
    image = Image.open(BytesIO(image_bytes))
    image_np = np.array(image)

    # Set new dimensions for the output image
    new_height, new_width = 500, 300  # Replace with your desired dimensions

    # Process the image based on the selected algorithm
    if algorithm_id == 'nearest-neighbour':
        processed_image_np = nearest_neighbour_interpolation(image_np, new_width, new_height)
    elif algorithm_id == 'bicubic':
        processed_image_np = bicubic_interpolation(image_np, new_width, new_height)
    elif algorithm_id == 'bilinear':
        processed_image_np = bilinear_interpolation(image_np, new_width, new_height)
    elif algorithm_id == 'fourier':
        processed_image_np = fourier_transform_super_resolution(image_np, new_width, new_height)
    elif algorithm_id == 'iterative-back-projection':
        processed_image_np = iterative_back_projection(image_np, new_width, new_height)
    elif algorithm_id == 'lanczos':
        processed_image_np = lanczos_resample(image_np, new_width, new_height)
    elif algorithm_id == 'non-local':
        processed_image_np = non_local_means_super_resolution(image_np, new_width, new_height)
    elif algorithm_id == 'total-variation':
        processed_image_np = total_variation_denoising(image_np, new_width, new_height)
    elif algorithm_id == 'wavelet':
        processed_image_np = wavelet_super_resolution_color(image_np, new_width, new_height)
    else:
        return jsonify({"error": "Invalid algorithm ID provided"}), 400

    processed_image = Image.fromarray(processed_image_np)

    # Save the processed image
    processed_image_filename = f"processed_image_{algorithm_id}.png"
    processed_image_path = os.path.join(PROCESSED_IMAGE_DIR, processed_image_filename)
    processed_image.save(processed_image_path)

    # Encode the processed image to base64 for API response
    buffered = BytesIO()
    processed_image.save(buffered, format="PNG")
    processed_image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return jsonify({
        "processedImage": f"data:image/png;base64,{processed_image_base64}",
        "savedPath": processed_image_path
    }), 200
    
    
if __name__ == '__main__':
    app.run(debug=True)
