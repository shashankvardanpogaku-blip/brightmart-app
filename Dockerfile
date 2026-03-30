# BrightMart Catalog App - Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies first (caching layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose application port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
