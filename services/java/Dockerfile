FROM maven:3-jdk-11 AS build
WORKDIR /home/app
COPY src /home/app/src
COPY pom.xml /home/app
RUN mvn -f /home/app/pom.xml clean package

FROM openjdk:11-jre
RUN mkdir -p /app/dependency-jars
WORKDIR /app
COPY --from=build /home/app/target /app/
COPY entrypointk8s.sh /entrypointk8s.sh
RUN chmod +x /entrypointk8s.sh
COPY extras/* /app/
EXPOSE 8080
CMD ["/entrypointk8s.sh"]
