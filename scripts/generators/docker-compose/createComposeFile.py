import argparse
from jinja2 import Environment, FileSystemLoader
import os
import yaml

debug_mode = False

def read_yaml(file_path):
    with open(os.path.expanduser(file_path), 'r') as file:
        # Parse the YAML file
        data = yaml.safe_load(file)
        return data

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

        template = env.get_template(template_path)

        rendered_content = template.render(yaml_data)
        
        with open(output_path, 'w') as output_file:
            output_file.write(rendered_content)
        
    else:
        raise Exception(f"Failed to read the configuration file {config_file}: The top-level structure is not a dictionary.")

try:   
    main()
except Exception as e:
    if not debug_mode:
        print(e)
    else:
        raise e
    exit(1)