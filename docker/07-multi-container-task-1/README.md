# Multi-Container Static App with Flask, Nginx and Alpine Logger

This project demonstrates how to run a mini application using **three Docker containers** that communicate via a **shared volume**.

- Manually wiring communication (without Docker Compose)


## Project Structure

multi-container-task-1/
  >shared/                  # Shared volume between containers
  >backend/                 # Flask app
	   >app.py
	   >requirements.txt
	   >Dockerfile
  >frontend/                # Nginx static frontend
	   >index.html
	   >Dockerfile

## Goal

The goal is to simulate a small app system with:

1. **Backend (Flask app)** — writes a file to a shared volume.
2. **Frontend (Nginx)** — serves a static HTML file that makes a request to the backend.
3. **Logger (Alpine container)** — periodically reads and prints the shared file contents to simulate logging or monitoring.

---

## Backend

Simple Flask app that saves a JSON file to `/data/message.json` in response to a request.

**Dockerfile (`backend/Dockerfile`):**

FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]

---

## Frontend

Nginx container that serves `index.html`, which sends a request to the Flask app.

**Dockerfile (`frontend/Dockerfile`):**

FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html

---

## Shared Volume

The `shared/` directory is mounted into all three containers at path `/data`.  
This allows:
- Backend to write `message.json` to `/data`
- Logger to read `/data/message.json`
- Frontend (optionally) to access shared content in future extensions.

---

## How to run

> Run the following commands from the root of the project (`multi-container-task-1/`):

### 1. Build the backend container
docker build -t my-flask-backend ./backend

### 2. Start the backend
docker run -d --name flask-backend -p 5003:5000 -v $(pwd)/shared:/data my-flask-backend

### 3. Build the frontend container
docker build -t my-nginx-frontend ./frontend

### 4. Start the frontend
docker run -d --name nginx-frontend -p 8083:80 my-nginx-frontend

### 5. Start the logger container
docker run -d --name logger -v $(pwd)/shared:/data alpine sh -c "while true; do cat /data/* 2>/dev/null; sleep 5; done"

## Test It

- Open http://localhost:8083 → This loads the frontend page.
- The frontend will make a request to http://localhost:5003.
- The backend writes data to `/data/message.json`.
- The logger container will periodically print the file content to the terminal.



------------------
------------------


## Why this logger command?

sh -c "while true; do cat /data/* 2>/dev/null; sleep 5; done"

Because:

- `sh -c` lets us pass a full shell script as a single string.
- `while true; do ... done` runs an **infinite loop**.
- `cat /data/*` reads all files in `/data`.
- `2>/dev/null` **suppresses error messages** if files don’t exist yet.
- `sleep 5` waits 5 seconds between checks to avoid overloading the system.

This pattern is a **simple and effective way to simulate logging** or monitoring file changes without any extra dependencies.

---




