#!/bin/bash
APP_SERVER_PORT=${APP_SERVER_PORT:-8080}
echo "Running server on :${APP_SERVER_PORT}"
APP_CONFIG="$(</config.json)" node index.js ${APP_SERVER_PORT}
