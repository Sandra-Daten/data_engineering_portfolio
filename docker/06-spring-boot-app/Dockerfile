# Dockerfile
FROM maven:3.9.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Kopiraj ceo Maven projekat
COPY demo/ .

# Build
RUN mvn clean package

# Kopiraj jar u deljeni folder unutar kontejnera
RUN mkdir -p /output && cp target/*.jar /output/app.jar

# Kad se run pokrene, kopiraj app.jar u mountovani volume
CMD ["ls", "/output"]



