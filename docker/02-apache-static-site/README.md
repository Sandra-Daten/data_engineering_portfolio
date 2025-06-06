# Apache Static Website in Docker


This project demonstrates how to run a simple static HTML website using the official `httpd` (Apache HTTP Server) Docker image.

## Task Description

Create a simple static web page (HTML) and make it accessible via the Apache HTTP server (`httpd`) inside a Docker container. Use the official `httpd` Docker image and expose the site externally.

## Project Structure

02-apache-static-site/
├── Dockerfile
├── index.html
└── run.sh


## Dockerfile

We use the official `httpd:2.4.63-alpine` image. The `index.html` file is copied into Apache's default `htdocs` directory.

```Dockerfile
FROM httpd:2.4.63-alpine
COPY ./index.html /usr/local/apache2/htdocs
EXPOSE 80

How to Run

You can use the run.sh script to build and run the container:

#!/bin/bash
docker build -t apache-static-site .
docker run -d -p 8080:80 apache-static-site

!!! Make sure to replace apache-static-site, apache-static-site-container, and 8080 with the image name, container name, and port number specific to your setup.

!!! To run the script, use:
chmod +x run.sh
./run.sh



After running the container, open your browser and visit:
http://localhost:8080
