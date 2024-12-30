#!/bin/bash
SERVICE_DEFAULT_PORT=${SERVICE_DEFAULT_PORT:-8080}
echo java -jar "javanode-1.0-SNAPSHOT.jar" "${SERVICE_DEFAULT_PORT}"
APP_CONFIG="$(</config.json)" java -jar "javanode-1.0-SNAPSHOT.jar" "${SERVICE_DEFAULT_PORT}"
