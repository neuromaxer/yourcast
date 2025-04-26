import json
import logging
from logging.handlers import RotatingFileHandler

import coloredlogs
import requests


def setup_logger(name, log_file, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    log_handler = RotatingFileHandler(filename=log_file, maxBytes=2000000, backupCount=5)
    log_handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    coloredlogs.install(level=level, logger=logger)

    return logger


def check_if_valid_url(url):
    # from https://stackoverflow.com/a/34266413
    prepared_request = requests.models.PreparedRequest()
    try:
        prepared_request.prepare_url(url, None)
        return True
    except requests.exceptions.MissingSchema:
        raise ValueError(f"Invalid URL: {url}")


def store_json(data: dict, filename: str) -> None:
    if filename[-5:] != ".json":
        filename += ".json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_json(filename: str) -> dict:
    if filename[-5:] != ".json":
        filename += ".json"

    with open(filename, "r") as f:
        data = json.load(f)
    return data
