import os
import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")


def get_config(argv=None) -> dict:
    with open(DEFAULT_CONFIG_PATH, "r") as file:
        return yaml.safe_load(file)
