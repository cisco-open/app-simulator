import yaml
import json
from jinja2 import Template
import argparse
import os

def renderService(templ,service_name, service_port, service_ext_port, service_type=""):
    with open(templ, 'r') as file:
        template = Template(file.read())
        context = {
            'service_name': service_name, 
            'service_port': service_port, 
            'service_ext_port': service_ext_port, 
            'service_type': service_type 
            }
        rendered_yaml = yaml.safe_load(template.render(context))
        return rendered_yaml

def renderConfigMap(templ, service_name, service_config):
    with open(templ, 'r') as file:
        template = Template(file.read())
        myconfig = service_config
        myconfig['name']=service_name
        context = {
            'service_name': service_name, 
            'service_config': json.dumps(myconfig), 
            }
        rendered_yaml = yaml.safe_load(template.render(context))
        return rendered_yaml 

def renderDeployment(templ, service_name, service_type, service_port):
    with open(templ, 'r') as file:
        template = Template(file.read())
        context = {
            'service_name': service_name, 
            'service_type': service_type,
            'service_port': service_port, 
            }
        rendered_yaml = yaml.safe_load(template.render(context))
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
        print(f"File not found: {os.path.expanduser(file_path)}")
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML file: {exc}")

def write_yaml(file_path, data):
    try:
        with open(file_path, 'w') as file:
            yaml.safe_dump(data, file, default_flow_style=False)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

# Example usage

parser = argparse.ArgumentParser(description='Process some configuration file.')
parser.add_argument(
    '--config', 
    type=str, 
    default='config.yaml',  # Set your default config file here
    help='Path to the configuration file (default: default_config.yaml)'
    )
args = parser.parse_args()
config_file = args.config
print(f'Using configuration file: {config_file}')

#file_path = 'config.yaml'  # Replace with your YAML file path
yaml_data = read_yaml(config_file)
application_services = {'java', 'dotnet', 'nodejs'} # adding php, pyhton
db_services = {'mysql'}  # adding mongo
loader_services = {'curl'}

if isinstance(yaml_data, dict):
    for key, value in yaml_data.items():
        if key== "k8s":
            print("Reading properties for k8s")
            print(f"Value: {value}")
        elif key == "services":
            #print(f"Value: {value}")
            for service, config in value.items():
                config['agent'] = False
                if config['type'] in application_services:
                    print(f"create Appplication Service of type {config['type']} named {service}") 
                    if config.get('port') != None:
                        write_yaml(f"./deployments/{service}-service-ext.yaml", renderService(templ=f"./templates/{key}/service.yaml.tmpl",service_name=service,service_port=8080,service_ext_port=config.get('port'),service_type="ext"))
                    write_yaml(f"./deployments/{service}-service.yaml",renderService(templ=f"./templates/{key}/service.yaml.tmpl",service_name=service,service_port=8080,service_ext_port=8080,service_type="int"))
                    write_yaml(f"./deployments/{service}-configmap.yaml",renderConfigMap(templ=f"./templates/{key}/config-map.yaml.tmpl",service_name=service, service_config=config))
                    write_yaml(f"./deployments/{service}-deployment.yaml",renderDeployment(templ=f"./templates/{key}/deployment.yaml.tmpl", service_name=service,service_type=config.get('type'),service_port=8080))
                elif config['type'] in db_services:
                    print(f"create DB Service of type {config['type']} named {service}")
                    write_yaml(f"./deployments/{service}-service.yaml",renderService(templ=f"./templates/{key}/db-service.yaml.tmpl",service_name=service,service_port=0,service_ext_port=0,service_type=config['type']))
                    write_yaml(f"./deployments/{service}-configmap.yaml",renderConfigMap(templ=f"./templates/{key}/config-map.yaml.tmpl",service_name=service, service_config=config))
                    write_yaml(f"./deployments/{service}-deployment.yaml",renderDeployment(templ=f"./templates/{key}/db-deployment.yaml.tmpl", service_name=service,service_type=config.get('type'),service_port=8080))
                else:
                    print(f"Unsupported service type detected {config['type']} named {service}")
        elif key == "loaders":
            for loader, config in value.items():
                if config['type'] in loader_services:
                    print (f"create loader service of type {config['type']} named {loader}")
                    with open('./templates/curl-deployment.yaml.tmpl', 'r') as file:
                        template = Template(file.read())
                        context = {
                            'service_name': loader, 
                            'service_type': config['type'],
                            'urls': " ".join(config['urls']),
                            'wait': config.get('wait',15),
                            'sleep': config.get('sleep',0.1)
                            }
                        rendered_yaml = yaml.safe_load(template.render(context))
                        write_yaml(f"./deployments/{loader}-deployment.yaml", rendered_yaml)
                else:
                    print(f"Unsupported loader type detected {config['type']} named {loader}")
        elif key == "databases":
            for service, config in value.items():
                config['agent'] = False
                if config['type'] in db_services:
                    print(f"create DB Service of type {config['type']} named {service}")
                    write_yaml(f"./deployments/{service}-service.yaml",renderService(templ=f"./templates/{key}/service.yaml.tmpl",service_name=service,service_port=0,service_ext_port=0,service_type=config['type']))
                    write_yaml(f"./deployments/{service}-configmap.yaml",renderConfigMap(templ=f"./templates/{key}/config-map.yaml.tmpl",service_name=service, service_config=config))
                    write_yaml(f"./deployments/{service}-deployment.yaml",renderDeployment(templ=f"./templates/{key}/deployment.yaml.tmpl", service_name=service,service_type=config.get('type'),service_port=8080))
                else:
                    print(f"Unsupported service type detected {config['type']} named {service}")
        else:
            print(f"found unsupported key {key} in config - ignoring")
else:
    print("The top-level structure is not a dictionary.")