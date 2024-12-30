#!/bin/bash
APP_SERVER_PORT=${APP_SERVER_PORT:-8080}
echo java -jar "javanode-1.0-SNAPSHOT.jar" "${APP_SERVER_PORT}"
APP_CONFIG="$(</config.json)" java -jar "javanode-1.0-SNAPSHOT.jar" "${APP_SERVER_PORT}"
