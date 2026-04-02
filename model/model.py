import logging
from ultralytics import YOLO
from pathlib import Path

class ShoeDetector:
    def __init__(self, model_path="best.pt"):
        logging.info("ShoeDetector class initialized")
        self.model = YOLO(model_path)
        logging.info(f"Model loaded from {model_path}")

    def predict(self, image_path, save_path="static/output.jpg"):
        """Run prediction and save output image with boxes drawn."""
        results = self.model.predict(source=image_path, save=False)
        detections = results[0]

        # Draw boxes on the image and save
        results[0].plot()  # modifies results[0].orig_img with boxes
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)  # make static folder
        results[0].orig_img.save(save_path)

        # Return the path for Flask to display
        return save_path

    def predict_classes(self, image_path):
        """Return list of detected shoe classes (like before)"""
        results = self.model.predict(source=image_path, save=False)
        detections = results[0]

        if len(detections.boxes) == 0:
            return ["No shoes detected"]

        detected_classes = []
        for cls in detections.boxes.cls:
            class_name = self.class_id_to_name(int(cls))
            detected_classes.append(class_name)

        return list(set(detected_classes))

    def class_id_to_name(self, class_id):
        class_mapping = {0: "Slipper", 1: "Sneaker"}
        return class_mapping.get(class_id, "Unknown")

    # Test with LOCAL image (important)
    predicted_classes = model.predict("test.jpg")

    logging.info(f"Detected shoes: {predicted_classes}")
