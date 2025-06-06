# Task 1 – Simple Web Application with Redis Counter

This project demonstrates the deployment of a simple dynamic web application using **Docker Compose**. The application counts and displays the number of visits to the main page by incrementing a counter stored in a Redis database.

## Components

The application is composed of two main services:

1. **Python Web Service**  
   A Flask-based web application that:
   - Displays a greeting
   - Shows the hostname
   - Tracks and displays the number of visits using Redis

2. **Redis Database**  
   A key-value store that keeps the count of page visits.

## Docker Setup

The deployment is handled using `docker-compose`. The following configurations are applied:

### Redis Service
- Uses the official `redis` base image.
- Maps container port `6379` to the host port `6379`.
- Mounts a volume to persist Redis data from the container’s `/data` directory.
- Attached to a custom Docker network named `webnet`.

### Python Web Service
- Built from a custom `Dockerfile`.
- Exposes the application on container port `80`, mapped to host port `8085`.
- Sets an environment variable `PERSON` with a custom greeting name.
- Connected to the same `webnet` network for communication with Redis.

## How to Run

1 -
Start the application with Docker Compose:
docker-compose up --build

2-
Open your browser and visit:
http://localhost:8085


