# **Curl loader quick start**
### *Load Testing with Application Simulator*

---

Looking to test your services under realistic conditions? Meet `Curl loader`,the lightweight load generation component built right into the [Application Simulator project](https://github.com/cisco-open/app-simulator) by Cisco Open Source.

Designed for speed, simplicity, and reliability, curl loader lets you simulate real world HTTP traffic using a config.json file.

## Configuration

To define load behavior, create a config.json file.

For example:

If you want to test how your API endpoint on the frontend service handles concurrent traffic, you can list it multiple times in the `urls` array and adjust the `sleep` and `wait` values accordingly to simulate the desired load pattern.

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

Each of the following parameters must be specified to control how the load is executed:

| field         | type          | description                              |
| ------------- | ------------- | ---------------------------------------- |
| Sleep         | number        |seconds to sleep between each request loop|
| Wait          | number        |initial wait time before the first request|
| URLs          | array         |list of service URLs to target            |

## Behavior Summary
- **Initial Delay**: Waits for the duration specified in wait (in seconds) before initiating any requests.
- **Request Execution**: Sends repeated HTTP GET requests to each URL in the list, automatically appending a `?unique_session_id=<uuid>` parameter to ensure each request is distinct.
- **Loop Interval**: Pauses for the duration specified in sleep (in seconds) between each full cycle of requests to all URLs.

## Dependencies

The script requires the following in its runtime environment:
- curl
- jq
- uuidgen (part of uuid-runtime or util-linux)

## Getting Started with Docker

### 1. Docker
Build the Docker image:  
```Bash 
   docker build -t curl-loader
```

Run the container:   
```Bash 
   docker run --rm -v $(pwd)/config.json:/config.json curl-loader
```

### 2. Docker Compose Integration
Use this block in your config.yaml:
```Yaml 
loaders: 
  user-1:    
   type: curl    
   wait: 0    
   sleep: 2    
   urls:      
     - http://frontend/upload      
     - http://frontend/upload      
     - http://frontend/upload


```
Generate the Docker Compose config:
```Bash 
  docker run --rm -v ${PWD}:/mnt \  
  ghcr.io/cisco-open/app-simulator-generators-docker-compose   
  --config /mnt/config.yaml \  
  --output /mnt/docker-compose.yaml
```
### 3. Example Scenario

Here is an example of `docker-compose.yaml` setup:

```Yaml 
services:  
  frontend:    
    image: ghcr.io/cisco-open/app-simulator-services-java:edge    
    ports:      
      - "3000:80"  
  user-1:    
    image: ghcr.io/cisco-open/app-simulator-loaders-curl:edge
```
After running `docker compose up `,the loader will continuously simulate user-traffic to frontend.

## Tracing with Jaeger

Combine this loader with OpenTelemetry instrumentation in your services and Jaeger to visualize traces flowing through your architecture.See the  [Observability with OpenTelemetry](https://github.com/cisco-open/app-simulator/blob/main/docs/tutorial/5-observability-with-opentelemetry.md) for details.