# Shoe Detection API (YOLO)

## Overview
This project is a deep learning-based API that detects types of shoes in images using a YOLO (You Only Look Once) object detection model.

The model classifies detected shoes into:
- Slipper
- Sneaker

The API is built using Flask and deployed with Docker, making it easy to run locally or on cloud platforms like Render.

---

## Features
- Upload an image via API
- Detect shoes in the image
- Return predicted class labels
- Fast inference using YOLO

---

## Model Details
- Model: YOLO (Ultralytics)
- Custom trained on shoe dataset
- Classes:
  - 0 → Slipper
  - 1 → Sneaker

---

## Setup Instructions (Run Locally with Docker)

### 1. Clone the repository
```bash
git clone <your-repo-link>
cd Yolo-deployment
