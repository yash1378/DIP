from flask import Flask, jsonify, request, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
import base64
import os
import sys
from PIL import Image
import io

# Add the root directory to sys.path to access 'processing' as a sibling directory to 'backend'
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

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
    # Get the JSON data from the request body
    data = request.get_json()
    
    # Check if the image and algorithm_id are present in the data
    if not data or 'imageData' not in data or 'algoId' not in data:
        return jsonify({"error": "No image file or algorithm ID provided"}), 400
    
    # Extract image and algorithm ID
    image_data = data['imageData']
    algorithm_id = data['algoId']
    
    # Print the extracted values to the backend terminal
    print(f"Received image: {image_data[:30]}...")  # Print a truncated version for security
    print(f"Algorithm ID: {algorithm_id}")

    # Decode the base64 image data
    header, encoded = image_data.split(',', 1)  # Split the header from the base64 data
    image_bytes = base64.b64decode(encoded)

    # Create a filename and save the image
    image_filename = f"uploaded_image_{algorithm_id}.png"  # Change extension as needed
    image_path = os.path.join('uploads', image_filename)  # Ensure 'uploads' directory exists

    # Save the image to the specified path
    with open(image_path, 'wb') as image_file:
        image_file.write(image_bytes)

    # Optionally, you can apply the specified algorithm here...

    return jsonify({"message": "Algorithm applied successfully", "image_path": image_path}), 200

    # if not algorithm_id:
    #     return jsonify({"error": "No algorithm ID provided"}), 400
    
    # if image.filename == '':
    #     return jsonify({"error": "No selected image file"}), 400
    
    # if image:
    #     filename = secure_filename(image.filename)
    #     filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #     image.save(filepath)
    
    #     if algorithm_id == 0:
    #         buf = bicubic.process_image(filepath)
    #     else:
    #         return jsonify({"error": "Invalid Algorithm ID"}), 500
        
    #     os.remove(filepath)
        
    #     return send_file(buf, mimetype='image/png', as_attachment=True, download_name='processed_image.png')


if __name__ == '__main__':
    app.run(debug=True)
