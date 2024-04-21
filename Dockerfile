# Use an official Python runtime as the base image
# Use an official Python runtime as a parent image
FROM python:3.10-slim

COPY . /app
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app

# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 80

# RUN mkdir ~/ .streamlit

# RUN cp config.toml ~/ .streamlit/config.toml

# RUN cp credentials.toml ~/ .streamlit/credentials.toml

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

ENTRYPOINT ["streamlit","run"]

CMD ["main.py"]


