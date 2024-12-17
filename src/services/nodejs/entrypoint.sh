#!/bin/bash
echo "Running server on :8080"
APP_CONFIG="$(</config.json)" node index.js 8080
#fi
