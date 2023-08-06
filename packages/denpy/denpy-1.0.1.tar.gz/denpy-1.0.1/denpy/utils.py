import json

def get_config_path() -> str:
    path = __file__.split('\\')
    path.pop(-1)
    path.append('config.json')
    return path

def get_token() -> str:
    with open(get_config_path(), 'r') as file:
        config = json.load(file)
    return config["token"]

def get_prefix() -> str:
    with open(get_config_path(), 'r') as file:
        config = json.load(file)
    return config["prefix"]
