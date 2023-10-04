import os
import pathlib

import yaml

API_ENV = os.getenv("api_env", "dev")
DIR = pathlib.Path(__file__).parent


with open(f"{DIR}/config.yaml", "r") as file:
    CONFIG = yaml.safe_load(file)[API_ENV]
