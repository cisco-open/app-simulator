FROM maven:3-jdk-14@sha256:aea55d01edac9df38eb17d19f6aabb55263f93cc8b23ac170a792922111ea487 AS build
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
