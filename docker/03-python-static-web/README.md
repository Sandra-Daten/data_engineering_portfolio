# Static Website with Python HTTP Server in Docker

This project demonstrates how to serve a static HTML page using Python's built-in `http.server` module within a Docker container.

## Project Structure

python-static-web/
 > Dockerfile
 > index.html
 > README.md


## Dockerfile

The Dockerfile uses the official Python image and serves the current directory using `http.server`.

```Dockerfile
FROM python:3
WORKDIR /app
COPY . .
CMD ["python3", "-m", "http.server"]


## How to run

1-
## To build the Docker image, run:
docker build -t my-python-static-web .

2-
## To run the container and expose the server to your host machine:
docker run --rm -d -p 8000:8000 --name python-static-web-service my-python-static-web

3-
## Once the container is running, you can access the static page by navigating to:
http://localhost:8000


