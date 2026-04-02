from ultralytics import YOLO
import os
import uuid

# Load model once
model = YOLO("model/best.pt")

def predict(image_path):
    # Run prediction
    results = model(image_path)

    # Ensure static folder exists
    os.makedirs("static", exist_ok=True)

    # Unique filename
    output_filename = f"result_{uuid.uuid4().hex}.jpg"
    output_path = os.path.join("static", output_filename)

    # Save image with detections
    results[0].save(filename=output_path)

    return output_path
