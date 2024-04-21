# Use an official Python runtime as the base image
FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6



