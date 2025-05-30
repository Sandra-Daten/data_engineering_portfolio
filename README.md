# Static Website with Nginx in Docker

## Task Description

Create a simple static website and serve it using the official Nginx Docker image. The website should be accessible both inside the Docker container and from outside (your host machine).

### Requirements:
- Use the official Nginx Docker image.
- Host a static HTML page.
- Ensure the website is accessible from your local machine through proper port mapping.

---

## Files structure on local machine

nginx-static-site:
- index.html
- Dockerfile

## How to run

1. enter the project directory
2. build the Docker image using the local Dockerfile
3. run the container with port mapping to expose the web server
4. then open your browser using:

##### The code:
   
1. cd path/to/nginx-static-site
2. docker build -t my-nginx-site .
3. docker run -d --name nginx-service-01 -p 8080:80 my-nginx-site
4. http://localhost:8080



(∩˃o˂∩)♡

