#!/bin/bash

PORT=8080
IMAGE_NAME=apache-static-site
CONTAINER_NAME=apache-static-site-container

# Pronađi kontejner koji koristi dati PORT na hostu
EXISTING_CONTAINER_ID=$(docker ps --format '{{.ID}} {{.Ports}}' | grep "0.0.0.0:$PORT->" | awk '{print $1}')

# Zaustavi i ukloni kontejner ako postoji
if [ -n "$EXISTING_CONTAINER_ID" ]; then
  echo "Stopping container using port $PORT..."
  docker stop $EXISTING_CONTAINER_ID
  docker rm $EXISTING_CONTAINER_ID
fi

# Build Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Pokreni novi kontejner
echo "Running container on port $PORT..."
docker run -d -p $PORT:80 --name $CONTAINER_NAME $IMAGE_NAME
