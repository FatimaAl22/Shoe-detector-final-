import logging
from ultralytics import YOLO


class ShoeDetector:
    def __init__(self, model_path="best.pt"):
        logging.info("ShoeDetector class initialized")
        self.model = YOLO(model_path)
        logging.info(f"Model loaded from {model_path}")

    def predict(self, image_path):
        """Run prediction on a local image file."""

        results = self.model.predict(source=image_path, save=False)
        detections = results[0]

        # No detections
        if len(detections.boxes) == 0:
            return ["No shoes detected"]  # always return list

        detected_classes = []

        for cls in detections.boxes.cls:
            class_name = self.class_id_to_name(int(cls))
            detected_classes.append(class_name)

        # Remove duplicates
        return list(set(detected_classes))

    def class_id_to_name(self, class_id):
        class_mapping = {
            0: "Slipper",
            1: "Sneaker"
        }
        return class_mapping.get(class_id, "Unknown")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    model = ShoeDetector("best.pt")

    # Test with LOCAL image (important)
    predicted_classes = model.predict("test.jpg")

    logging.info(f"Detected shoes: {predicted_classes}")