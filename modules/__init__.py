import json
import logging.config
from os import path, remove
from pathlib import Path

from modules.infrastructure.file_manager import FileManager

FileManager(Path(__file__).resolve().parent.parent).make_directory_if_not_exist("Logs")


if path.isfile("Logs/logger.log"):
    remove("Logs/logger.log")

with open("modules/log_config.json", "r") as log_config:
    config_dict = json.load(log_config)

logging.config.dictConfig(config_dict)
