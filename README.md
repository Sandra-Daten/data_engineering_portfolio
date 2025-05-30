# Static Website with Nginx in Docker

## Task Description

Create a simple static website and serve it using the official Nginx Docker image. The website should be accessible both inside the Docker container and from outside (your host machine).

### Requirements:
- Use the official Nginx Docker image.
- Host a static HTML page.
- Ensure the website is accessible from your local machine through proper port mapping.

---

## Files structure on local machine

nginx-static-site/
- index.html
- Dockerfile

## How to run

##### Enter the project directory
cd path/to/nginx-static-site

##### Build the Docker image using the local Dockerfile
docker build -t my-nginx-site .

##### Run the container with port mapping to expose the web server

docker run -d --name nginx-service-01 -p 8080:80 my-nginx-site

##### Then open your browser and go to:

http://localhost:8080


Thanx for visiting :)

