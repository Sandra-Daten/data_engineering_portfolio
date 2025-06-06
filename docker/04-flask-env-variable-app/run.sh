#!/bin/bash

PORT=5050
IMAGE_NAME=flask-dynamic-app
CONTAINER_NAME=flask-dynamic-app-container

# Stop and remove any container using the port
EXISTING_CONTAINER_ID=$(docker ps | grep "$PORT" | awk '{print $1}')

if [ -n "$EXISTING_CONTAINER_ID" ]; then
  echo "Stopping container using port $PORT..."
  docker stop $EXISTING_CONTAINER_ID
  docker rm $EXISTING_CONTAINER_ID
fi

# Build Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Run container with optional PERSON env var passed from host
echo "Running container on port $PORT..."
docker run -d -p $PORT:5050 --name $CONTAINER_NAME -e PERSON="${PERSON:-Marko}" $IMAGE_NAME
