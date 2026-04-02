from ultralytics import YOLO
import os
import uuid

# Load model once
model = YOLO("model/best.pt")

def predict(image_path):
    # Run prediction
    results = model(image_path)

    output_path = os.path.join("static", f"result_{uuid.uuid4().hex}.jpg")

    # Save image with detections
    results[0].save(filename=output_path)

    return output_path
