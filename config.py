import yaml

_config = None

def config(reload: bool = False) -> dict:
    global _config
    if not _config or reload:
        with open('config.yaml', 'r') as file:
            _config = yaml.safe_load(file)
    return _config