FROM maven:3-jdk-11 AS build
WORKDIR /home/app
COPY src /home/app/src
COPY pom.xml /home/app
RUN mvn -f /home/app/pom.xml clean package

FROM openjdk:11-jre

LABEL org.opencontainers.image.source=https://github.com/cisco-open/app-simulator
LABEL org.opencontainers.image.description="java service for app-simulator"
LABEL org.opencontainers.image.licenses=BSD-3-Clause

RUN mkdir -p /app/dependency-jars
WORKDIR /app
COPY --from=build /home/app/target /app/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY extras/* /app/
EXPOSE 8080
CMD ["/entrypoint.sh"]
