import os
from flask import Flask, request, render_template
import urllib.request

from model.model import ShoeDetector

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/v1/predict", methods=["POST"])
def predict():
    image_url = request.form.get("image_url")

    if not image_url:
        return "No URL provided"

    # Save input image
    input_path = "static/input.jpg"
    urllib.request.urlretrieve(image_url, input_path)

    # Run model and save output image
    output_path = shoe_detector.predict(input_path)  # returns "static/output.jpg"

    return f"""
        <h2>Detection Result</h2>
        <img src="/{output_path}" width="500">
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

