#!/bin/bash
env CUSTOM_CODE_DIR="./scripts" APP_CONFIG="$(<../examples/frontend.json)" nodemon index.js 8080
