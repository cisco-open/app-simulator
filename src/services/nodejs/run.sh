#!/bin/bash
env CUSTOM_CODE_DIR="./scripts" APP_CONFIG="$(<../../../examples/frontend.json)" node --watch index.js 8080
