# Flask Dynamic Web Application in Docker

This project serves a simple dynamic web application built with Python and Flask inside a Docker container.

## Description

The application is implemented in `app.py` and uses the Flask framework, installed via `requirements.txt`.  
The displayed content on the web page is controlled by the environment variable `PERSON`, which by default is set to **Marko** inside the Docker image.

## Folder structure

flask-env-variable-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── run.sh
└── README.md


## How to Build and Run

Use the provided `run.sh` script to build and run the Docker container.

!!! To run the script, use:
chmod +x run.sh
./run.sh

You can override the default `PERSON` environment variable by setting it before running the script:

```bash
export PERSON=YourName
./run.sh
