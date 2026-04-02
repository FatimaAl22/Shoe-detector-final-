from flask import Flask, request, render_template
import os
import urllib.request
from model.model import predict   

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def run_prediction():
    image_url = request.form.get("image_url")

    if not image_url:
        return "No URL provided"

    filepath = "input.jpg"
    urllib.request.urlretrieve(image_url, filepath)

    output_path = predict(filepath)

    return f"""
    <h2>Detection Result</h2>
    <img src="/static/{filename}" width="500">
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
