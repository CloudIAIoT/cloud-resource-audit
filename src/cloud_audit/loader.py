import json
from pathlib import Path

def load_resources(path):
    with open(path, "r") as file:
        data = json.load(file)

    return data

if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    path = BASE_DIR/ "data" / "inventory_valid.json"

    try:
        data = load_resources(path)
        print(f"Resources loaded: {len(data["resources"])}")

    except FileNotFoundError:
        print("The file was not found.")

    except json.JSONDecodeError:
        print("The file is an invalid JSON file")

    except ValueError as error:
        print(error)
