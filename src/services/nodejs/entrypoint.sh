#!/bin/bash
SERVICE_DEFAULT_PORT=${SERVICE_DEFAULT_PORT:-8080}
echo "Running server on :${SERVICE_DEFAULT_PORT}"
APP_CONFIG="$(</config.json)" node index.js ${SERVICE_DEFAULT_PORT}
