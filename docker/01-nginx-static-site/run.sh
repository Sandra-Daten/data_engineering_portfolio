#!/bin/bash

# Script to build and run a simple static site using Nginx in Docker

# Set variables
IMAGE_NAME="my-nginx-site"
CONTAINER_NAME="nginx-service-01"
PORT=8080

# Build Docker image
echo "🛠 Building Docker image..."
docker build -t $IMAGE_NAME .

# Stop and remove any existing container with the same name
echo "🧹 Cleaning up any existing container..."
docker rm -f $CONTAINER_NAME 2>/dev/null

# Run container with port mapping
echo "🚀 Starting container..."
docker run -d --name $CONTAINER_NAME -p $PORT:80 $IMAGE_NAME

# Show success message
echo "✅ Static site is running at: http://localhost:$PORT"
