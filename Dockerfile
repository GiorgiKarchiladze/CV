# Base image for Python
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install system dependencies required for MySQL and Flask
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements.txt
# If you don't have a requirements.txt, you can skip this part or install dependencies directly in RUN
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask
EXPOSE 8080

# Command to run the Flask app
CMD ["python", "app.py"]
