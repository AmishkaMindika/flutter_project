# Use an official Python base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory to the container
COPY . .

# Install system dependencies (for pydub, speech recognition, etc.)
RUN apt-get update && apt-get install -y ffmpeg portaudio19-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Start the Flask server
CMD ["python", "voice_recorder.py"]
