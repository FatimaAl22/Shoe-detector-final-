# app.py
import os
import logging
import urllib.request
from flask import Flask, request, jsonify
from model.model import ShoeDetector
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize model
model = ShoeDetector("model/best.pt")  # Adjust path if needed

@app.route("/")
def home():
    return "Shoe Detector API is live!"

@app.route("/predict", methods=["POST"])
def predict():
    """
    Accepts either:
    1. JSON with 'image_url'
    2. Form-data with file 'image'
    """
    image_path = None

  
    if 'image' in request.files:
        file = request.files['image']
        if file.filename == '':
            return jsonify({'detected_classes': ['No file selected']})
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)

    elif request.json and 'image_url' in request.json:
        image_url = request.json['image_url']
        filename = secure_filename(image_url.split("/")[-1])
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            urllib.request.urlretrieve(image_url, image_path)
        except Exception as e:
            logging.error(f"Failed to download image: {e}")
            return jsonify({'detected_classes': ['Failed to load image']})

    else:
        return jsonify({'detected_classes': ['No image provided']})

    # Run prediction
    try:
        detected_classes = model.predict(image_path)
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return jsonify({'detected_classes': ['Prediction failed']})

    return jsonify({'detected_classes': detected_classes})

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
