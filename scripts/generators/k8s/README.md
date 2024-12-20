# Introduction

This project is intended to replace the run.sh and build.sh orginally included in APM game. It creates deployment files to let APM games run on kubernetes. It creates the required deployment, service and a config-map which holds the configuration for every service defined.

It handles the deployment of databases and loaders as well as custom serices. The AppDynamics specific part has been removed from the images and the build process.
As there is no content or syntax check, you need to make sure that the templates render propery and are valid for k8s. The generated yamls should be comlpliant according to yaml specs, but there is no check for validity againt k8s. 

## Usage
to run the generator, you'll need to have a working python environment with the depencies outlined in 'requirements.txt' installed. This can be your global environment or a venv. For more information how to create a venv (highly recommended) please see the [official pyhton docs](https://docs.python.org/3/library/venv.html)

### Create manifests
run the command
```shell
python3 createManifests.py [--config myconfigfile.yaml] [--debug]
```

If successful, the script will render a number of yaml files for k8s deployment in the ./deployments folder.
**Existing files will be overwritten!**

## Info

## Template Variables

## Custom Services
You can create your own custom service types, and the script will try to generate k8s yaml files for you. There is absolutely no check on the content other than we're producing valid yaml files.

To create a custom service, all you need to do is creating a subfolder in the ./templates directory with the name of your service_type.
Adapt the deployments to your need, you can also introduce new template variables, which you can define within the app-simulator config. It is your responsibility to adapt config and templates to your needs.

### Example of custom service definition

```yaml
custom1:
  cust_svc1:
    type: redis
    config:
      - my config 1
      - my config 2
    password: secret
```

this will look for 3 template files in `./templates/custom1' named 'configmap.yaml.j2', 'deployment.yaml.j2', 'service.yaml.j2'. The generator will attempt to render all 3 of them, regardless if they are required or not. Worst case, create an empty valid configuration template.

## Status
draft documentation