from flask import Flask, request, render_template
import os
import urllib.request
from model.model import predict   # ✅ correct import

app = Flask(__name__)

# ---------- HOME PAGE ----------
@app.route("/")
def index():
    return render_template("index.html")


# ---------- PREDICT ----------
@app.route("/predict", methods=["POST"])
def run_prediction():
    image_url = request.form.get("image_url")

    if not image_url:
        return "No URL provided"

    # Ensure folders exist
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("static", exist_ok=True)

    # Download image
    input_path = os.path.join("uploads", "input.jpg")
    try:
        urllib.request.urlretrieve(image_url, input_path)
    except:
        return "Failed to load image"

    # Run YOLO
    output_path = predict(input_path)

    # Extract filename for static serving
    filename = os.path.basename(output_path)

    # Show result in browser
    return f"""
    <h2>Detection Result</h2>
    <img src="/static/{filename}" width="500">
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
