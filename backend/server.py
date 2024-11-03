from flask import Flask, jsonify, request, send_file
from werkzeug.utils import secure_filename
import os
from PIL import Image
import io

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from processing import bicubic

app = Flask(__name__)

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
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image = request.files['image']
    algorithm_id = request.form.get('algorithm_id')
    
    if not algorithm_id:
        return jsonify({"error": "No algorithm ID provided"}), 400
    
    if image.filename == '':
        return jsonify({"error": "No selected image file"}), 400
    
    if image:
        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)
    
        if algorithm_id == 0:
            buf = bicubic.process_image(filepath)
        else:
            return jsonify({"error": "Invalid Algorithm ID"}), 500
        
        os.remove(filepath)
        
        return send_file(buf, mimetype='image/png', as_attachment=True, download_name='processed_image.png')

if __name__ == '__main__':
    app.run(debug=True)