from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from io import BytesIO
import numpy as np
from nearest_neighbour_interpolation import nearest_neighbour_interpolation  # Adjust based on your directory structure
from bicubic import bicubic_interpolation
from video import process_video
from bilinear import resize_image_bilinear
from lanczos import lanczos_resample
from wavelet import wavelet_super_resolution_color
from totalvariation import upscale_with_tv
from iteractivebackprojection import iterative_back_projection  # Import the function
from fourier import fourier_transform_super_resolution
from non_local import non_local_means_super_resolution
from edgeDetection import sobel_edge_detection_color
from gammacorrection import gamma_correction
from adjust_saturation import saturation_adjust_color
from gaussian_blur import gaussian_blur_color
from entropy import calculate_entropy
from contrast import calculate_contrast
from snr import calculate_snr
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
CORS(app, origins=["http://localhost:3000"])
  # Enable CORS for all routes
app.config['CORS_HEADERS'] = 'Content-Type'


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
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

@app.route('/api/list_post_processing_steps')
@cross_origin()
def get_post_processing_methods():
    methods = [
        {
            "id": 1,
            "name": "Gaussian Blur",
            "description": "A filter that smooths the image by averaging neighboring pixels weighted by a Gaussian function.",
            "complexity": "O(n^2)",
            "category": "Image Processing",
            "tags": ["blur", "smoothing", "filtering", "gaussian"]
        },
        {
            "id": 2,
            "name": "Saturation Adjustment",
            "description": "A technique for altering the intensity of colors in an image, enhancing or reducing saturation.",
            "complexity": "O(n)",
            "category": "Color Correction",
            "tags": ["color", "adjustment", "saturation"]
        },
        {
            "id": 3,
            "name": "Edge Detection",
            "description": "A technique used to identify the boundaries of objects within images by detecting changes in intensity.",
            "complexity": "O(n)",
            "category": "Image Processing",
            "tags": ["edge detection", "filtering", "image processing"]
        },
        {
            "id": 4,
            "name": "Gamma Correction",
            "description": "A technique used to adjust the brightness of an image to compensate for non-linear lighting.",
            "complexity": "O(n)",
            "category": "Image Enhancement",
            "tags": ["brightness", "correction", "gamma", "image enhancement"]
        }
    ]
    return jsonify(methods)



@app.route('/api/video', methods=['POST'])
@cross_origin()
def apply_video():
    data = request.get_json()
    
    # Check if video data is provided
    if not data or 'video' not in data:
        return jsonify({"error": "No video data provided"}), 400

    video_data_base64 = data['video']
    algo = data['algorithm']  # The algorithm id (e.g., 1 for Bicubic Interpolation, 2 for Bilinear Interpolation)
    print(f"Algorithm ID: {algo}")
    
    try:
        # Decode the base64 string to bytes
        video_data = base64.b64decode(video_data_base64.split(",")[1])

        # Process the video and get the processed frames
        processed_video_data = process_video(video_data, algo)

        # Return the processed video as a Base64 string
        return jsonify({
            "message": "Video processed successfully",
            "processed_video": f"data:video/mp4;base64,{processed_video_data}"
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while processing the video"}), 500
    

@app.route('/api/apply-algorithm', methods=['POST'])
@cross_origin()
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
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    image_np = np.array(image)
    print(len(image_np))
    print(len(image_np[0]))
    print(len(image_np[0][0]))
    
    # Set new dimensions for the output image
    new_height, new_width = 1000, 1000  # Replace with your desired dimensions
    print('algorithm_id:', algorithm_id)
    if algorithm_id == 1 or algorithm_id == 5 or algorithm_id == 7:
        new_height, new_width = 500, 300  # Replace with your desired dimensions
    else:
        new_height, new_width = 1000, 1000  # Replace with your desired dimensions
        
        
    # Process the image based on the selected algorithm
    if algorithm_id == 1:
        processed_image_np = bicubic_interpolation(image_np, new_width, new_height)
    elif algorithm_id == 2:
        # processed_image_np = resize_image_bilinear(image, new_width, new_height)
        processed_image_np = resize_image_bilinear(image_np, new_width, new_height)
    elif algorithm_id == 3:
        # processed_image_np = fourier_transform_super_resolution(image, new_width, new_height)
        processed_image_np = fourier_transform_super_resolution(image_np, new_width, new_height)
    elif algorithm_id == 4:
        # processed_image_np = iterative_back_projection(image, new_width, new_height)
        processed_image_np = iterative_back_projection(image_np, new_width, new_height)
    elif algorithm_id == 5:
        # processed_image_np = lanczos_resample(image, new_width, new_height)
        processed_image_np = lanczos_resample(image_np, new_width, new_height)
    elif algorithm_id == 6:
        processed_image_np = nearest_neighbour_interpolation(image_np, new_width, new_height)
    elif algorithm_id == 7:
        # processed_image_np = non_local_means_super_resolution(image, new_width, new_height)
        processed_image_np = non_local_means_super_resolution(image_np, new_width, new_height)
    elif algorithm_id == 8:
        # processed_image_np = upscale_with_tv(image, new_width, new_height)
        processed_image_np = upscale_with_tv(image_np, new_width, new_height)
    elif algorithm_id == 9:
        # processed_image_np = wavelet_super_resolution_color(image, new_width, new_height)
        print(image_np.shape)
        processed_image_np = wavelet_super_resolution_color(image_np, new_width, new_height)
    else:
        print(algorithm_id)
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
    

@app.route('/api/apply-processing', methods=['OPTIONS','POST'])
@cross_origin()
def apply_process():
    if request.method == 'OPTIONS':
            response = jsonify()
            # Manually set CORS headers for the pre-flight OPTIONS request
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'  # Allow only the frontend origin
            response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'  # Allow POST and OPTIONS methods
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Allow Content-Type header
            print('Aaaahhhhhh')
            return response
    print("hello")
    data = request.get_json()
    
    if not data or 'imageData' not in data or 'processId' not in data:
        return jsonify({"error": "No image file or algorithm ID provided"}), 400

    image_data = data['imageData']
    algorithm_id = data['processId']
    
    # print(image_data)
    print(algorithm_id)

    # Decode base64 image
    header, encoded = image_data.split(',', 1)
    image_bytes = base64.b64decode(encoded)
    image = Image.open(BytesIO(image_bytes))
    print("Image size:", image.size)
    image_np = np.array(image)
    print(image_np)
    processed_image_np=1

    if algorithm_id==3:
        processed_image_np= sobel_edge_detection_color(image_np)
    elif algorithm_id==4:
        processed_image_np= gamma_correction(image_np,1.5)
    elif algorithm_id==1:
        processed_image_np=gaussian_blur_color(image_np)
    elif algorithm_id==2:
        processed_image_np=saturation_adjust_color(image_np)
    print(processed_image_np)

    processed_image = Image.fromarray(processed_image_np)

    # # Save the processed image
    processed_image_filename = f"processed_image_{algorithm_id}.png"
    processed_image_path = os.path.join(PROCESSED_IMAGE_DIR, processed_image_filename)
    processed_image.save(processed_image_path)

    # Encode the processed image to base64 for API response
    buffered = BytesIO()
    processed_image.save(buffered, format="PNG")
    processed_image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    # print(processed_image_base64)
    return jsonify({
        "hello":"world",
        "processed_image":processed_image_base64
    }), 200
    
    

@app.route('/api/apply-metrics', methods=['OPTIONS','POST'])
@cross_origin(origins=["http://localhost:3000"])
def apply_metrics():
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    # Get JSON data from request
    try:
        data = request.get_json()
    #     if not isinstance(data, list) or len(data) < 2:
    #         raise ValueError("Invalid data structure. Expected a list with at least two items.")
    except Exception as e:
        return jsonify({"error": "Failed to parse request data", "details": str(e)}), 400

    # Extract the first and second items
    try:
        # print(len(data))

        first_item = data['images']
        second_item = data['processType']
        print(second_item)
        # return

        # Access properties
        image_data1 = first_item[0]
        image_data2 = first_item[1]
        # print(first_item[0])
        # return
        # second_name = second_item.get('name')
        # image_data2 = second_item.get('data')
        # process_type = second_item.get('processType', None)

        if not image_data1 or not image_data2:
            raise ValueError("Missing image data in the input.")
    except Exception as e:
        return jsonify({"error": "Failed to extract data from request", "details": str(e)}), 400

    # Decode and process images
    try:
        # First image
        header, encoded = image_data1.split(',', 1)
        image_bytes = base64.b64decode(encoded)
        image = Image.open(BytesIO(image_bytes))
        image_np1 = np.array(image)

        # Second image
        header, encoded = image_data2.split(',', 1)
        image_bytes = base64.b64decode(encoded)
        image = Image.open(BytesIO(image_bytes))
        image_np2 = np.array(image)

        print("First image size:", image_np1.shape)
        print("Second image size:", image_np2.shape)
    except Exception as e:
        return jsonify({"error": "Failed to process images", "details": str(e)}), 400

    # Perform processing
    try:
        if second_item == 'contrast':
            c1 = calculate_contrast(image_np1)
            c2 = calculate_contrast(image_np2)
            return jsonify({
                "a": c1,
                "b": c2
            }), 200
        elif second_item == 'snr':
            s1 = calculate_snr(image_np1)
            s2 = calculate_snr(image_np2)
            return jsonify({
                "a":s1,
                "b":s2
            }),200
        elif second_item == 'entropy':
            e1 = calculate_entropy(image_np1)
            e2 = calculate_entropy(image_np2)
            return jsonify({
                "a":e1,
                "b":e2
            }),200
        # Other processing types can go here
        return jsonify({
            "message": "Process type not implemented",
            "process_type": second_item
        }), 400
    except Exception as e:
        return jsonify({"error": "Failed during processing", "details": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
