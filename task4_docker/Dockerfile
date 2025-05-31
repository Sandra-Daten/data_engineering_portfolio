#rebuild-trigger
FROM maven:3.9.9-eclipse-temurin-8 AS builder
WORKDIR /app
COPY demo/ .
RUN mvn clean package
RUN mkdir -p /output && cp target/*.jar /output/app.jar

