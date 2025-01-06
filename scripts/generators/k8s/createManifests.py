import yaml
import json
from jinja2 import Template
import argparse
import os

debug_mode = False

def renderDeployment2(templ_type, config, serviceName):
    with open(f"./templates/{templ_type}/deployment.yaml.j2", 'r') as file:
        config.update(serviceName=serviceName)
        #debug_print(f"Rendering Deployment {serviceName}")
        #debug_print(json.dumps(config, indent=2))
        template = Template(file.read())
        rendered_yaml = yaml.safe_load(template.render(config))
        return rendered_yaml 

def renderService2(templ_type, config, serviceName):
    with open(f"./templates/{templ_type}/service.yaml.j2", 'r') as file:
        config.update(serviceName=serviceName)
        #debug_print(f"Rendering Service {serviceName}")
        #debug_print(json.dumps(config, indent=2))
        template = Template(file.read())
        rendered_yaml = yaml.safe_load(template.render(config))
        #debug_print(f"Rendered Template:\n{yaml.dump(rendered_yaml)}")
        return rendered_yaml     

def renderConfigMap2(templ_type, config, serviceName):
    with open(f"./templates/{templ_type}/configmap.yaml.j2", 'r') as file:
        config.update(serviceName=serviceName)
        debug_print(f"Rendering ConfigMap {serviceName}")
        debug_print(json.dumps(config, indent=2))
        context = {
            'serviceName': serviceName, 
            'serviceConfig': json.dumps(config), 
        }
        template = Template(file.read())
        rendered_yaml = yaml.safe_load(template.render(context))
        debug_print(f"Rendered Template:\n{yaml.dump(rendered_yaml)}")
        return rendered_yaml   

def merge_dicts(dict1, dict2):
    """
    Recursively merge two dictionaries.
    If keys are present in both and values are dictionaries, merge them.
    Otherwise, the value from the second dictionary will overwrite the value from the first.
    """
    if dict1 == None:
        result = {}
    else:
        result = dict1.copy()  # Start with dict1's keys and values
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # If both values are dictionaries, merge them recursively
            result[key] = merge_dicts(result[key], value)
        else:
            # Otherwise, overwrite the value with the one from dict2
            result[key] = value
    return result
        
# Function to read a YAML file
def read_yaml(file_path):
    try:
        with open(os.path.expanduser(file_path), 'r') as file:
            # Parse the YAML file
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        debug_print(f"File not found: {os.path.expanduser(file_path)}")
    except yaml.YAMLError as exc:
        debug_print(f"Error parsing YAML file: {exc}")

def write_yaml(file_path, data):
    try:
        with open(file_path, 'w') as file:
            yaml.safe_dump(data, file, default_flow_style=False)
    except Exception as e:
        debug_print(f"An error occurred while writing to the file: {e}")

def debug_print(*args, **kwargs):
    if debug_mode:
        print(*args, **kwargs)

# Example usage
def main():
    global debug_mode 
    parser = argparse.ArgumentParser(description='Process some configuration file.')
    parser.add_argument(
        '--config', 
        type=str, 
        default='config.yaml',  # Set your default config file here
        help='Path to the configuration file (default: config.yaml)'
        )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    args = parser.parse_args()
    config_file = args.config
    debug_mode = args.debug
    debug_print(f'Using configuration file: {config_file}')

    #file_path = 'config.yaml'  # Replace with your YAML file path
    yaml_data = read_yaml(config_file)
    application_services = {'java', 'dotnetcore', 'nodejs'} # adding php, pyhton
    db_services = {'mysql'}  # adding mongo
    loader_services = {'curl'}

    if isinstance(yaml_data, dict):
# merge the global and k8s configs from simpler access
# some ugly code hacked togeter, so that it works for MVP
# TODO: clean up code
        globalConfig = yaml_data.get("global", {})
        keys_to_keep = {  "appName","imageNamePrefix","imageVersion","k8s"} 
        gconfig = {key: globalConfig[key] for key in keys_to_keep if key in globalConfig}
        debug_print(f"gconfig: gconfig")
        globalConfigK8s = gconfig.get("k8s", {})
        debug_print("k8sconfig: {globalConfigK8s}")
        gconfig.pop("k8s", None)
        globalConfig = merge_dicts(gconfig, globalConfigK8s)
        yaml_data.pop("global", None)
        debug_print(f"Global Config:\n", json.dumps(globalConfig, indent=2))
# Ok, lets start to parse through the services and render the k8s deployments
        for key, value in yaml_data.items():
            if key == "services":
                #debug_print(f"Value: {value}")
                for service, config in value.items():
                    config['agent'] = False
                    if config['type'] in application_services:
                        config=merge_dicts(globalConfig, config)
                        print(f"create Appplication Service of type {config['type']} named {service}") 
                        write_yaml(f"./deployments/{service}-configmap.yaml",renderConfigMap2(key, config, service))
                        write_yaml(f"./deployments/{service}-deployment.yaml",renderDeployment2(key,config, service))
                        if config.get('exposedPort', None) != None:
                            debug_print(f"ExposedPort: {config.get('exposedPort')}")
                            write_yaml(f"./deployments/{service}-service-ext.yaml",renderService2(key, config, service))
                            config2 = config
                            config2.pop('exposedPort', None)
                            # if port is set, we do need two service, one of type cluserIP and one of type Loadbalancer. As I'm unable to render a yaml template with 2 documents I need to workaround
                            write_yaml(f"./deployments/{service}-service.yaml",renderService2(key, config, service))
                        else:
                            write_yaml(f"./deployments/{service}-service.yaml",renderService2(key, config, service))
                    else:
                        print(f"Unsupported service type detected {config['type']} named {service}")
            elif key == "loaders":
                for loader, config in value.items():
                    if config['type'] in loader_services:
                        print (f"create loader service of type {config['type']} named {loader}")
                        context=merge_dicts(globalConfig, config)
                        context['serviceName'] = loader 
                        context['type'] = config['type']
                        context['urls'] = " ".join(config['urls'])
                        print(f"Context to be passed: {context}")
                        write_yaml(f"./deployments/{loader}-configmap.yaml",renderConfigMap2(key, config, loader))
                        write_yaml(f"./deployments/{loader}-deployment.yaml",renderDeployment2(key, context, loader))
                        # There is no need to create a service for a loadgenerator at this point in time
                    else:
                        print(f"Unsupported loader type detected {config['type']} named {loader}")
            elif key == "databases":
                for service, config in value.items():
                    config['agent'] = False
                    if config['type'] in db_services:
                        config=merge_dicts(globalConfig, config)
                        print(f"create DB Service of type {config['type']} named {service}")
                        write_yaml(f"./deployments/{service}-configmap.yaml",renderConfigMap2(key, config, service))
                        write_yaml(f"./deployments/{service}-deployment.yaml",renderDeployment2(key,config, service))
                        if config.get('exposedPort', None) != None:
                            write_yaml(f"./deployments/{service}-service-ext.yaml",renderService2(key, config, service))
                            config2 = config
                            config2.pop('exposedPort', None)
                            write_yaml(f"./deployments/{service}-service.yaml",renderService2(key, config, service))
                        else:
                            write_yaml(f"./deployments/{service}-service.yaml",renderService2(key, config, service))
                    else:
                        print(f"Unsupported service type detected {config['type']} named {service}")
            else:
#                
#TODO: works but is totally unsupported
#
                print(f"found unsupported key {key} in config - try rendering deployment, service and configmap")
                try :
                    for service, config in value.items():
                        config=merge_dicts(globalConfig, config)
                        write_yaml(f"./deployments/{service}-configmap.yaml",renderConfigMap2(key, config, service))
                        write_yaml(f"./deployments/{service}-deployment.yaml",renderDeployment2(key,config, service))
                        write_yaml(f"./deployments/{service}-service-ext.yaml",renderService2(key, config, service))
                except Exception as e:
                    print(f"An error occured, skipping: {e}")
    else:
        print("The top-level structure is not a dictionary.")

if __name__ == '__main__':
    main()