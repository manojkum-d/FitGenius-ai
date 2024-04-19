# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8501

# Run the Streamlit app when the container launches
CMD ["streamlit", "run", "app.py"]

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6


