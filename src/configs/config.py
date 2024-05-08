import os

from pyaml_env import parse_config, BaseConfig


CONFIG_FILE_NAME = "config.yaml"

# This is the path to the config file.
current_directory = os.path.dirname(os.path.abspath(__file__))
directory = os.path.join(current_directory, os.pardir, os.pardir)

settings = BaseConfig(parse_config(os.path.normpath(directory) + f"/{CONFIG_FILE_NAME}"))
