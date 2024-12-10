#!/bin/bash
echo java -jar "javanode-1.0-SNAPSHOT.jar" 8080
APP_CONFIG="$(</config.json)" java -jar "javanode-1.0-SNAPSHOT.jar" 8080
