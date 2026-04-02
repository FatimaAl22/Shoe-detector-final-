from flask import Flask, request, send_file, jsonify
from model.model import ShoeDetector
import os

app = Flask(__name__)

# Initialize model
shoe_detector = ShoeDetector("model/best.pt")  # adjust path if needed

@app.route("/")
def home():
    return "Shoe Detector API is live!"

@app.route("/predict", methods=["POST"])
def predict():
    """
    Expects JSON with either:
    { "image_url": "<url>" }  or
    { "image_path": "<path_in_repo>" }  (optional, for testing)
    """

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    image_url = data.get("image_url")
    image_path = data.get("image_path")
    save_path = "/tmp/detection_result.jpg"

    detected_classes = shoe_detector.predict(
        image_path=image_path,
        image_url=image_url,
        save_path=save_path
    )

    response = {"detected_classes": detected_classes}

    # Return image if detection exists
    if os.path.exists(save_path):
        response["image_file"] = "detection_result.jpg"  # file can be downloaded separately

    return jsonify(response)

if __name__ == "__main__":
    # Use PORT environment variable if set (Render sets $PORT automatically)
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
