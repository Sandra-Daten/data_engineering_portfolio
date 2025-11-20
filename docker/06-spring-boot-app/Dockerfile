# Dockerfile
FROM maven:3.9.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy entire Maven project
COPY demo/ .

# Build
RUN mvn clean package

# Copy jar in the shared volume in the container
RUN mkdir -p /output && cp target/*.jar /output/app.jar

# After run, copy app.jar in mounted volume
CMD ["ls", "/output"]



