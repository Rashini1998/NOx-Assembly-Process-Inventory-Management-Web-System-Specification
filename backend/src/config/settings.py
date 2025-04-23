import os
import yaml

def load_config():
    env = os.getenv('ENV', 'development')

    with open('backend/src/config/config.yaml', 'r') as file:
        all_config = yaml.safe_load(file)

    return all_config.get(env)
