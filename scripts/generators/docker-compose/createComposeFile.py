import argparse
from deepmerge import always_merger
import inflect
from jinja2 import Environment, FileSystemLoader
import os
import yaml
# Initialize inflect engine
p = inflect.engine()


debug_mode = False

defaultValues = {
    "imageNamePrefix": "ghcr.io/cisco-open/",
    "imageNameSuffix": "latest",
    "defaultPorts": {
        "services": 80, # this is different from the "default default" on purpose. 
        "databases": 5432,
        "loaders": 6000 # not used
    },
    # Keep the default ports for each service type here
    # We need them to verify in the docker compose generation if they have been
    # changed by the user.
    "_defaultDefaultPorts": {
        "services": 8080,
        "databases": 5432,
        "loaders": 6000
    }
}

def plural_to_singular(word):
    return p.singular_noun(word) or word

def read_yaml(file_path):
    with open(os.path.expanduser(file_path), 'r') as file:
        # Parse the YAML file
        data = yaml.safe_load(file)
        return data

def render_compose_file(template, data, defaultValues):
    globalVars = data.get('global', {})

    config = {
            "global": always_merger.merge(defaultValues, globalVars),
            "scopes": {
                "services": data.get('services', {}),
                "databases": data.get('databases', {}),
                "loaders": data.get('loaders', {}),
            }
    }

    return template.render(config)

def main():
    global debug_mode
    global defaultValues
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
    parser.add_argument(
        '--template',
        type=str,
        default='docker-compose.j2',
        help='Path to the Jinja2 template file (default: docker-compose.j2)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='docker-compose.yaml',
        help='Path to the output file (default: docker-compose.yaml)'
    )
    args = parser.parse_args()
    config_path = args.config
    debug_mode = args.debug
    template_path = args.template
    output_path = args.output

    yaml_data = read_yaml(config_path)
    if isinstance(yaml_data, dict):
        env = Environment(loader=FileSystemLoader('.'))

        env.filters['singularize'] = plural_to_singular

        template = env.get_template(template_path)

        rendered_content = render_compose_file(template, yaml_data, defaultValues)
        
        with open(output_path, 'w') as output_file:
            output_file.write(rendered_content)
        
    else:
        raise Exception(f"Failed to read the configuration file {config_file}: The top-level structure is not a dictionary.")


if __name__ == "__main__":
    try:   
        main()
    except Exception as e:
        if not debug_mode:
            print(e)
        else:
            raise e
        exit(1)