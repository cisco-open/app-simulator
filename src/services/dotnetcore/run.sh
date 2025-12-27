#!/bin/bash
env APP_CONFIG="$(<../../../examples/backend.json)" dotnet run
