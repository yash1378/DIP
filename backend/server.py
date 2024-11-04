from flask import Flask, jsonify, request, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
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

if __name__ == '__main__':
    app.run(debug=True)
