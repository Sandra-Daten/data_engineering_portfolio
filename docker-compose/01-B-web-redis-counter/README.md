# Task 1 – Web Application + Redis (Docker)

## Description

This task consists of containerizing a simple Flask-based web application that displays the number of visits using Redis as a data store. The goal is to manage environment variables, connect services via Docker networks, use multiple Compose files for environment-specific configurations, and understand volume handling in Docker.

---

## Project Structure

01-B-web-redis-counter/
> app.py # Flask application
> requirements.txt # Python dependencies
> .env # Environment variables file
> web.yml # Docker Compose file for development
> web.prod.yml # Override file for production environment
> redis.yml # Docker Compose file for Redis service


---

## Core Steps

### 1. Isolate Environment Variables
Environment variable `PERSON` is extracted into a separate `.env` file:
```dotenv
PERSON=Sara
```
### 2.Addapt the environment keyword in web.yml file 
```dotenv
services:
  web:
    build: .
    ports:
      - "8085:80"
    volumes:
      - .:/data
    env_file:
      - .env  
    networks:
      - webnet

networks:
  webnet:
    external: true
```

### 3. Organize redis.yml file independantly
```dotenv
services:
  redis:
    image: "redis:alpine"
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - webnet

volumes:
  redis_data:

networks:
  webnet:
    external: true
```

## How to run

### 1. Start Redis Service Separately
docker-compose -f redis.yml up -d

### 2. Connect Web App to Redis
docker-compose -f web.yml up -d

### 3. Specify Compose File Manually
Multiple Compose files are combined manually during startup:
docker-compose -f web.yml -f web.prod.yml up -d

### 4. Override Configuration Using Inheritance - word.prod.yml
The web.prod.yml file overrides certain properties such as port mapping and environment variables for production:
```dotenv
services:
  web:
    ports:
      - "80:80"
    environment:
      - PERSON=Production User
```

### 5. Delete the named volume upon executing the "docker-compose down" command
docker-compose -f redis.yml down -v


### Access

Development environment: http://localhost:8085
Production environment: http://localhost













