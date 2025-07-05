import random
import time
import yaml
import os


def random_delay(delay_range=(1, 3)):
    delay = random.uniform(*delay_range)
    time.sleep(delay)

def load_sources_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "sources.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    # Return as dict by id for easy lookup
    return {src['id']: src for src in data['sources']}
