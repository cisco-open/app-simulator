#!/bin/bash
env APP_CONFIG="$(<../backend.json)" mvn -e compile exec:java
