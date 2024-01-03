# Use an NVIDIA CUDA base image with CUDA 11.1
FROM nvidia/cuda:11.1.1-cudnn8-runtime-ubuntu20.04

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
        libpng-dev \
        libfreetype6-dev \
        libharfbuzz-dev \
        libgl1-mesa-glx \
        python3.8 \
        python3-pip \
        python3.8-dev \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools
RUN python3 -m pip install --upgrade pip setuptools wheel

# Install additional dependencies (if needed) before copying requirements.txt
# RUN apt-get install -y ...

# Set up and install Python dependencies
WORKDIR /app
COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

# Copy the application code into the container
COPY . /app

# Expose the required port
EXPOSE 8000

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app

# Switch to the non-root user
USER appuser

# Command to run the application
CMD ["torchrun", "server.py"]
