import json
import logging.config
from os import path, remove

if path.isfile("Logs/logger.log"):
    remove("Logs/logger.log")

with open("modules/log_config.json", 'r') as log_config:
    config_dict = json.load(log_config)

logging.config.dictConfig(config_dict)
