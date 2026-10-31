import json
from pathlib import Path

def load_resources(path):
    with open(path, "r") as file:
        data = json.load(file)

    return data

