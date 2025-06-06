#!/bin/bash

# Configuration
FLASK_IMAGE_NAME=flask-redis-app
FLASK_CONTAINER_NAME=flask-redis-app
REDIS_CONTAINER_NAME=redis-db
REDIS_PORT=6379
FLASK_PORT=5000
NETWORK_NAME=webnet
REDIS_VOLUME=redis-data

# Build Flask slike
echo "Building Flask image..."
docker build -t $FLASK_IMAGE_NAME .

# If network does not exist create it
if ! docker network ls | grep -q "$NETWORK_NAME"; then
  echo "🔗 Creating Docker network: $NETWORK_NAME"
  docker network create $NETWORK_NAME
fi

echo "Starting Redis container..."
docker run -d \
  --name $REDIS_CONTAINER_NAME \
  --network $NETWORK_NAME \
  -p 6379:$REDIS_PORT \
  -v $(pwd)/$REDIS_VOLUME:/data \
  redis:alpine


echo "Starting Flask container..."
docker run -d \
  --name $FLASK_CONTAINER_NAME \
  --network $NETWORK_NAME \
  -p 5001:$FLASK_PORT \
  -e PERSON=Marli \
  $FLASK_IMAGE_NAME
