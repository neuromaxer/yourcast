import json

import requests


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
