# Voting App

This project is a simple multi-service application demonstrating how to orchestrate containers using Docker Compose. It consists of 5 interconnected services that simulate a real-time voting system.

## Services Overview

| Service      | Description                                      | Tech Stack              | Port |
|--------------|--------------------------------------------------|--------------------------|------|
| `voting-app` | Frontend web app where users vote (Cats vs Dogs) | Python + Flask           | 5001 |
| `redis`      | Stores votes in-memory                           | Redis (official image)   | -    |
| `worker`     | Background processor to move data from Redis to DB | Java + Maven.          | -    |
| `db`         | PostgreSQL database storing final results        | PostgreSQL (official)    | 5432 |
| `result-app` | Displays the voting results live                 | Node.js + Express        | 5002 |


## Project Structure

02-voting-app/ 
> vote                 # Python Flask app for voting
> result               # Node.js app for result display
> worker               # Java worker service
> docker-compose.yml
> README.md

---

## How to Run the Project

### 1. Start the application
```
docker-compose up -d
```
### 2. Access the services
Voting app (vote here): http://localhost:5001
Results app (view results): http://localhost:5002

