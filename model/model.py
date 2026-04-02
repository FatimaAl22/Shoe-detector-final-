import logging
from ultralytics import YOLO
import requests
from PIL import Image
from io import BytesIO
import os

class ShoeDetector:
    def __init__(self, model_path="best.pt"):
        logging.info("Initializing ShoeDetector...")
        self.model = YOLO(model_path)
        logging.info(f"Model loaded from {model_path}")

    def predict(self, image_path=None, image_url=None, save_path="result.jpg"):
        """
        Run prediction on a local image or image URL.
        Returns a list of detected classes.
        """

        if image_url:
            # Download image from URL
            try:
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content)).convert("RGB")
                image_path = "/tmp/temp_image.jpg"
                img.save(image_path)
            except Exception as e:
                logging.error(f"Failed to download image: {e}")
                return ["Failed to load image"]

        if not image_path or not os.path.exists(image_path):
            logging.error("No valid image provided for prediction")
            return ["No image provided"]

        # Run YOLO prediction
        results = self.model.predict(source=image_path, save=False)
        detections = results[0]

        # If no shoes detected
        if len(detections.boxes) == 0:
            return ["No shoes detected"]

        detected_classes = []
        for cls in detections.boxes.cls:
            detected_classes.append(self.class_id_to_name(int(cls)))

        # Save image with bounding boxes
        results[0].plot().save(save_path)

        return list(set(detected_classes))

    def class_id_to_name(self, class_id):
        class_mapping = {
            0: "Slipper",
            1: "Sneaker"
        }
        return class_mapping.get(class_id, "Unknown")

# Only run test when executing directly
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    detector = ShoeDetector("best.pt")
    classes = detector.predict(image_path="test.jpg")
    logging.info(f"Detected shoes: {classes}")
