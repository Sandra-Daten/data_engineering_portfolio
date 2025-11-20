# Voting App - Multi-Container Deployment with Docker

This project demonstrates a complete multi-service voting application deployed using Docker containers without Docker Compose. It includes backend and frontend services, real-time data processing, persistent storage, and inter-container communication using custom Docker networks.

## Project Structure


voting-app/
│
├── vote/                  # Python Flask app for voting
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── result/                # Node.js app for displaying vote results
│   ├── server.js
│   ├── package.json
│   └── Dockerfile
│
├── worker/                # Java (previously .NET) app that transfers data from Redis to PostgreSQL
│   └── Dockerfile.j
│
├── shared/                # Persistent volume for PostgreSQL
│
└── README.md


## Services

 Service      Technology    Description |
|-------------|--------------|-------------|
 vote         - Python Flask - Frontend for voting between cats and dogs |
 redis        - Redis        - Queue for storing incoming votes |
 worker       - Java         - Background service that reads votes from Redis and saves them to PostgreSQL |
 db           - PostgreSQL   - Persistent database |
 result       - Node.js      - Frontend for displaying real-time vote results |

## Networks

Two Docker networks are used:

- **front-tier**: Connects frontend-facing services (vote, result)
- **back-tier**: Connects all services for backend communication (vote, result, worker, redis, db)

## Dockerfile Notes

--- `worker/Dockerfile.j`

This file is used to build the worker image based on Java instead of .NET. 
No need to use another dockrfile  called 'Dockerfile' in this directory.


## Build and Run Instructions

### 1. Create Docker Networks

```bash
docker network create front-tier
docker network create back-tier
```

### 2. Run Redis

```bash
docker run -d \
  --name redis \
  --network back-tier \
  -p 6379:6379 \
  redis
```

### 3. Run PostgreSQL

```bash
docker volume create pgdata

docker run -d \
  --name db \
  --network back-tier \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=votes \
  -v pgdata:/var/lib/postgresql/data \
  postgres
```

### 4. Run `vote` Service

```bash
docker build -t vote-image ./vote

docker run -d \
  --name vote \
  --network back-tier \
  --network-alias vote \
  --network front-tier \
  -p 5001:80 \
  -v $(pwd)/vote:/app \
  vote-image
```

### 5. Run `result` Service

```bash
docker build -t result-image ./result

docker run -d \
  --name result \
  --network back-tier \
  --network-alias result \
  --network front-tier \
  -p 5000:80 \
  -p 5858:5858 \
  -v $(pwd)/result:/app \
  result-image
```

### 6. Run `worker` Service

```bash
docker build -t worker-image -f ./worker/Dockerfile.j ./worker

docker run -d \
  --name worker \
  --network back-tier \
  worker-image
```

## Accessing the App

- **Vote Interface:** http://localhost:5001  
- **Results Dashboard:** http://localhost:5000


