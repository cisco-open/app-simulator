FROM maven:3-jdk-11@sha256:805f366910aea2a91ed263654d23df58bd239f218b2f9562ff51305be81fa215 AS build
WORKDIR /home/app
COPY src /home/app/src
COPY pom.xml /home/app
RUN mvn -f /home/app/pom.xml clean package

FROM openjdk:11-jre@sha256:356949c3125c4fa8104745e7ea92bd995da4567634e6599b470d2f972d13e0e2

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
