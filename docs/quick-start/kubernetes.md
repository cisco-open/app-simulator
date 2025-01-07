# kubernetes quick start

You can turn an [app sim config](../specification/README.md) into kubernetes
manifest files using the [k8s generator](../../scripts/generators/k8s/).

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
    port: 3000
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

This will create a set of YAML files in the `deployments` folder of your current
working directory.

To deploy the simulation into your cluster run

```shell
kubectl apply -f deployments/
```

This will bring up the three services (`frontend`, `processing` and
`virus-scanner`) and a loader (`user-1`).
