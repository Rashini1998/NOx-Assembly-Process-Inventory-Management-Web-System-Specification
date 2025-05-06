# def load_config():
#     env = os.getenv('ENV', 'development')

#     with open('backend/src/config/config.yaml', 'r') as file:
#         all_config = yaml.safe_load(file)
#     return all_config.get(env)

import os
import yaml

def load_config():
    env = os.getenv('ENV', 'development').upper()
    print(f"Loading config for environment: {env}")

    # Get the current file directory and form an absolute path to the config.yaml
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'config.yaml')

    # Load the config.yaml
    with open(config_path, 'r') as file:
        all_config = yaml.safe_load(file)
    print(f"All config loaded: {all_config}")
    return all_config.get(env)


def get_refresh_interval():
    config = load_config()
    return config.get('REFRESH_INTERVAL_MINUTES',1)
