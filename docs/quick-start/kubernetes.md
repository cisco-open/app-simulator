# kubernetes quick start

You can turn an [app sim config](../specification/README.md) into kubernetes
manifest files using the [k8s generator](../../scripts/generators/k8s/).

## Generate k8s manifest files

The generator is available as docker image and you can retrieve it by running

```shell
docker pull ghcr.io/cisco-open/app-simulator-generators-k8s:latest
```

To try it out, create the a file called `config.yaml` with the following content
in a new folder:

```yaml
services:
  frontend:
    type: java
    exposedPort: 3000
    endpoints:
      http:
        /upload:
          - http://processing/magicByte
          - http://processing/virus
  processing:
    type: java
    endpoints:
      http:
        /magicByte:
          - cache,128
        /virus:
          - http://virus-scanner/scan
  virus-scanner:
    type: nodejs
    endpoints:
      http:
        scan:
          - sleep,1500
          - call: error,500,Scan failed
            probability: 0.1
          - sleep,500
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

To generate manifest files for kubernetes from this file run

```shell
docker run --rm -t -i -v ${PWD}/deployments:/app/deployments -v ${PWD}:/mnt ghcr.io/cisco-open/app-simulator-generators-k8s:latest --config /mnt/config.yaml
```

## Run application simulation

The last step has created a set of YAML files in the `deployments` folder of
your current working directory.

To deploy the simulation into your cluster run

```shell
kubectl apply -f deployments/
```

This will bring up the three services (`frontend`, `processing` and
`virus-scanner`) and a loader (`user-1`). Run `kubectl get pods` to verify that
all services are up and running.

The loader will continuously load from the `/upload` endpoint. You can also
reach that endpoint yourself, either by opening <http://localhost:3000/upload>
in the browser or by running the following:

```shell
curl http://localhost:3000/upload
```

The files in `deployments/` that were generated now work independent of the
generator. You can use them wherever you want and you can modify them to your
needs.
