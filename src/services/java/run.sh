#!/bin/bash
env APP_CONFIG="$(<../examples/backend.json)" mvn -e compile exec:java
