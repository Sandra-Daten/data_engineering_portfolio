# Spring Boot Docker Multi-Container Deployment

This project demonstrates how to build and run a Spring Boot application using two separate Docker containers:

Builder container: Uses Maven to build the Spring Boot application and outputs the resulting .jar file to a shared volume.
Runner container: Runs the Spring Boot application using the built .jar file from the shared volume.

## Project Structure

/
├── Dockerfile.builder   # Dockerfile for build container (Maven)
├── Dockerfile.runner    # Dockerfile for runner container (Java runtime)
├── demo/                # Spring Boot application source code
└── shared/              # Shared volume directory for the built .jar file

## How to Run

**1. Build the builder image**
docker build -f Dockerfile -t spring-boot-builder .

**2. Run the builder container**
docker run --rm -v $(pwd)/shared:/output spring-boot-builder

This will build the app and copy the app.jar file into the shared/ folder on your host machine.

**3. Build the runner image**
docker build -f "Dockerfile 2" -t spring-boot-runner .

**4. Run the runner container**
docker run --rm -v $(pwd)/shared:/app spring-boot-runner

The runner container will execute the .jar file (app.jar) located in the shared volume and start the Spring Boot application.

## Notes

-- The shared volume shared/ must exist on your host machine and will be used to transfer the .jar file from the builder container to the runner container.
-- The builder container uses Maven to compile and package the Spring Boot app.
-- The runner container uses Eclipse Temurin JDK 17 to run the .jar file.
--Make sure to expose ports in the Spring Boot app if you want to access it from outside the container (configure in application.properties and add -p flag in docker run).