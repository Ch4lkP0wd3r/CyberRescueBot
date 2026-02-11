# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (needed for some python packages like Pillow/PDF)
# libgl1-mesa-glx might be needed if you use opencv, but for now just basics
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a volume for the database and assets to persist data
VOLUME ["/app/data"]

# Define environment variable (Can be overridden at runtime)
# ENV TELEGRAM_TOKEN=your_token_here

# Run bot.py when the container launches
CMD ["python", "bot.py"]
