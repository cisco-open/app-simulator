# Curl loader

You can simulate your project by continuously send HTTP requests from config.json file to a list of target services by this lightweight load generator component within this [Application Simulator project](https://github.com/cisco-open/app-simulator)


# Configuration - config.json

You have to create a config.json file to define the load behaviour .For example:
```JSON
{ 
  "sleep": 2,
  "wait": 5,
  "urls": [
    "http://frontend/upload",
    "http://frontend/upload",
    "http://frontend/upload"
  ]
}
```

These are fields you have to define ,
## Sleep 
**Type** : number
Seconds to sleep between each request loop

## Wait 
**Type** : number
Initial wait time before the first request

## URLs
**Type** : array
List of service URLs to target



## Behavior Summary
- Waits for `wait` seconds before starting.
- Repeatedly sends HTTP GET requests to each URL with`?unique_session_id=<uuid>`.
- Waits `sleep` seconds between each loop.

## Dependencies

The script requires the following in its runtime environment:

-curl
-jq
-uuidgen (part of uuid-runtime or util-linux)

# Usage

## 1.Docker
Build:
```Bash docker build -t curl-loader```
Run:
```Bash docker run --rm -v $(pwd)/config.json:/config.json curl-loader```

## 2.Docker Compose Integration
Use this block in your config.yaml:
```Yaml loaders:
  user-1:
    type: curl
    wait: 0
    sleep: 2
    urls:
      - http://frontend/upload
      - http://frontend/upload
      - http://frontend/upload
```
Then generate the Docker Compose config:
```Bash docker run --rm -v ${PWD}:/mnt \
  ghcr.io/cisco-open/app-simulator-generators-docker-compose \
  --config /mnt/config.yaml \
  --output /mnt/docker-compose.yaml
```
##Example Scenario
Your `docker-compose.yaml` may include services like:

```Yaml services:
  frontend:
    image: ghcr.io/cisco-open/app-simulator-services-java:edge
    ports:
      - "3000:80"
  user-1:
    image: ghcr.io/cisco-open/app-simulator-loaders-curl:edge
```
After running `docker compose up `,the loader will continuously simulate user-traffice to `frontend`.

## Tracing with Jaeger

Combine this loader with OpenTelemetry instrumentation in your services and Jaeger to visualize traces flowing through your architecture.See the 1.  [Observability with OpenTelemetry](https://github.com/cisco-open/app-simulator/blob/main/docs/tutorial/5-observability-with-opentelemetry.md) for details.