# Tutorial 1: Two services

> [!NOTE]
>
> This tutorial is work in progress.

Make sure that you have either completed the
[docker compose](../quick-start/docker-compose/README.md) or
[kubernetes](../quick-start/kubernetes.md) quick start.

In this tutorial you will learn more about the structure of an application
simulation configuration (app sim config) and how you can influence the behavior
of your services.

Create a new empty directory, in this directory, create a `config.yaml` file
with the following content:

```yaml
services:
  frontend:
    type: java
    endpoints:
      http:
        /list:
          - http://backend/list/items
  backend:
    type: java
    endpoints:
      http:
        /list/items:
          - slow,1024
loaders:
  user1:
    type: curl
    wait: 5
    sleep: 1
    urls:
      - http://frontend/list
```

This configuration file defines two services and one loader:

1. The service `frontend` is a Java-based application, that provides an HTTP
   endpoint called `/list`. When this endpoint gets called, it will send a HTTP
   request to the URL `http://backend/list/items`
2. The service `backend` is also a Java-based application that provides an HTTP
   endpoint, called `/list/items`. When this endpoind gets called, it will some
   "slow" code for ~1024 milliseconds.
3. The loader `user1` is a [curl](https://curl.se/)-based load generator. It
   will wait 5 seconds after start up and then call the URL
   `http://frontend/list` repeatedly. It will wait 1 second between each call.

Use your preferred [generator](../../scripts/generators/) to deploy this
simulation:

- For docker compose run

  ```shell
  docker run --rm -t -i -v ${PWD}:/mnt cisco-open/app-simulator-generators-docker-compose --config /mnt/config.yaml --output /mnt/docker-compose.yaml
  docker compose up
  ```

- For kubernetes run

  ```shell
  docker run --rm -t -i -v ${PWD}/deployments:/app/deployments -v ${PWD}:/mnt ghcr.io/cisco-open/app-simulator-generators-k8s:latest --config /mnt/config.yaml
  kubectl apply -f deployments/
  ```
