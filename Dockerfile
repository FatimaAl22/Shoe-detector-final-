FROM python:3.10

WORKDIR /app

# Install system dependencies (for YOLO / OpenCV)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# IMPORTANT: Render uses dynamic port
ENV PORT=10000

# Expose port
EXPOSE 10000

# Run app
CMD ["python", "app.py"]

