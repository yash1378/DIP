from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from io import BytesIO
import numpy as np
from nearest_neighbour_interpolation import nearest_neighbour_interpolation  # Adjust based on your directory structure
from bicubic import bicubic_interpolation
from bilinear import resize_image_bilinear
from lanczos import lanczos_resample
from wavelet import wavelet_super_resolution_color
from totalvariation import upscale_with_tv
from iteractivebackprojection import iterative_back_projection  # Import the function
from fourier import fourier_transform_super_resolution
from non_local import non_local_means_super_resolution
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
os.makedirs(PROCESSED_IMAGE_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app, origins=["http://localhost:2000"])
  # Enable CORS for all routes
app.config['CORS_HEADERS'] = 'Content-Type'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEBUG'] = False  # Turn off debugging

@app.route('/')
@cross_origin()
def hello():
    return "Hello, World!"

@app.route('/api/list_super_resolution_methods')
@cross_origin()
def get_methods():
    methods = [
        {"id": 1, "name": "Bicubic Interpolation", "description": "A high-quality resampling technique using cubic splines.", "complexity": "O(n^2)", "category": "Image Processing", "tags": ["interpolation", "cubic", "resampling"]},
        {"id": 2, "name": "Bilinear Interpolation", "description": "A linear resampling technique.", "complexity": "O(n)", "category": "Image Processing", "tags": ["interpolation", "linear", "resampling"]},
        {"id": 3, "name": "Fourier Transform", "description": "A method to transform a signal into its frequency components.", "complexity": "O(n log n)", "category": "Signal Processing", "tags": ["frequency", "transform", "signal"]},
        {"id": 4, "name": "Iterative Backprojection", "description": "An iterative algorithm for reconstructing images.", "complexity": "O(n^2)", "category": "Image Reconstruction", "tags": ["reconstruction", "backprojection", "iterative"]},
        {"id": 5, "name": "Lanczos Resampling", "description": "A high-quality resampling technique using sinc functions.", "complexity": "O(n log n)", "category": "Image Processing", "tags": ["resampling", "sinc", "interpolation"]},
        {"id": 6, "name": "Nearest Neighbor Interpolation", "description": "A simple interpolation technique.", "complexity": "O(1)", "category": "Image Processing", "tags": ["interpolation", "nearest", "resampling"]},
        {"id": 7, "name": "Non-Local Means", "description": "A noise reduction algorithm.", "complexity": "O(n^2)", "category": "Image Denoising", "tags": ["denoising", "filtering", "non-local"]},
        {"id": 8, "name": "Total Variation Denoising", "description": "An image denoising technique.", "complexity": "O(n log n)", "category": "Image Denoising", "tags": ["denoising", "variation", "filtering"]},
        {"id": 9, "name": "Wavelet Transform", "description": "A transformation technique for compression and denoising.", "complexity": "O(n)", "category": "Signal Processing", "tags": ["wavelet", "transform", "compression"]}
    ]
    return jsonify(methods)

@app.route('/api/apply-algorithm', methods=['OPTIONS', 'POST'])
# @cross_origin()
def apply_algorithm():
    if request.method == 'OPTIONS':
        response = jsonify()
        # Manually set CORS headers for the pre-flight OPTIONS request
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'  # Allow only the frontend origin
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'  # Allow POST and OPTIONS methods
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Allow Content-Type header
        print('Aaaahhhhhh')
        return response
    print('Fuck')
    data = request.get_json()
    
    if not data or 'imageData' not in data or 'algoId' not in data:
        return jsonify({"error": "No image file or algorithm ID provided"}), 400

    image_data = data['imageData']
    algorithm_id = data['algoId']

    # Decode base64 image
    header, encoded = image_data.split(',', 1)
    image_bytes = base64.b64decode(encoded)
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    image_np = np.array(image)
    print(len(image_np))
    print(len(image_np[0]))
    print(len(image_np[0][0]))

    # Set new dimensions for the output image
    print('algorithm_id:', algorithm_id)
    if algorithm_id == 1 or algorithm_id == 5 or algorithm_id == 7:
        new_height, new_width = 500, 300  # Replace with your desired dimensions
    else:
        new_height, new_width = 1000, 600  # Replace with your desired dimensions

    # Process the image based on the selected algorithm
    if algorithm_id == 1:
        processed_image_np = bicubic_interpolation(image_np, new_width, new_height)
    elif algorithm_id == 2:
        processed_image_np = resize_image_bilinear(image_np, new_width, new_height)
    elif algorithm_id == 3:
        processed_image_np = fourier_transform_super_resolution(image_np, new_width, new_height)
    elif algorithm_id == 4:
        processed_image_np = iterative_back_projection(image_np, new_width, new_height)
    elif algorithm_id == 5:
        processed_image_np = lanczos_resample(image_np, new_width, new_height)
    elif algorithm_id == 6:
        processed_image_np = nearest_neighbour_interpolation(image_np, new_width, new_height)
    elif algorithm_id == 7:
        processed_image_np = non_local_means_super_resolution(image_np, new_width, new_height)
    elif algorithm_id == 8:
        processed_image_np = upscale_with_tv(image_np, new_width, new_height)
    elif algorithm_id == 9:
        print(image_np.shape)
        processed_image_np = wavelet_super_resolution_color(image_np, new_width, new_height)
    else:
        print(algorithm_id) 
        return jsonify({"error": "Invalid algorithm ID provided"}), 400
    print('Finallllyyyyy')

    print(processed_image_np)
    print(len(processed_image_np))
    print(len(processed_image_np[0]))
    print(len(processed_image_np[0][0]))
    processed_image = Image.fromarray(processed_image_np)
    print(processed_image)

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
        "savedPath": processed_image_path,
        "new_height": new_height,
        "new_width": new_width
    }), 200

if __name__ == '__main__':
    app.run(debug=False)

# @app.errorhandler(500)
# def internal_server_error(e):
#     response = jsonify({"error": "Internal Server Error", "message": str(e)})
#     response.status_code = 500
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     print('Aaaaahhhhh')
#     return response
