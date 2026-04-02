FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Remove hardcoded PORT if you want Render to assign it dynamically
# ENV PORT=10000

# Use shell form so $PORT is expanded correctly
CMD gunicorn --bind 0.0.0.0:$PORT app:app




