# Dockerfile
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app folder into container
COPY . .

# Expose Flask port
EXPOSE 5000

# Default command to run Flask
CMD ["python", "app.py"]
