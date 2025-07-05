import yaml
import os


def get_config():
    config_path = os.path.join("config", "settings.yaml")
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
