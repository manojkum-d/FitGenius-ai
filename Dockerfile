# Use an official Python runtime as the base image
FROM python:3.10-slim

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8081


# Run app.py when the container launches
CMD ["python", "main.py"]

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6



