import os
import logging
from flask import Flask, request, jsonify

from model.model import ShoeDetector

app = Flask(__name__)

# Load model once
model_path = "best.pt"
model = ShoeDetector(model_path)

logging.basicConfig(level=logging.INFO)


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "name": "Shoe Detection API",
        "version": "1.0",
        "endpoint": "/v1/predict",
        "method": "POST",
        "input": "form-data with key = 'file'"
    })


@app.route("/v1/predict", methods=["POST"])
def predict():
    logging.info("Predict request received!")

    # Check file
    if "file" not in request.files:
        return jsonify({"error": "Please upload an image file"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save file temporarily
    filepath = "temp.jpg"
    file.save(filepath)

    try:
        # Run prediction
        prediction = model.predict(filepath)

        return jsonify({
            "predicted_class": prediction
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

    finally:
        # Clean up
        if os.path.exists(filepath):
            os.remove(filepath)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

