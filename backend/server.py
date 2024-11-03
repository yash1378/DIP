from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/api/available_super_resolution_methods')
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

if __name__ == '__main__':
    app.run(debug=True)