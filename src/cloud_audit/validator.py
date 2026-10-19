
def validate_inventory(data):

    if not isinstance(data, dict):
        raise ValueError("The inventory must be a Python dictionary")

    required_inventory_keys = {"inventory_version", "resources"}
    missing_keys = required_inventory_keys - data.keys()
    if missing_keys:
        raise ValueError(f"The following keys are missing: {missing_keys}")

    if data["inventory_version"] != "1.0":
        raise ValueError("Unsupported inventory version")

    if not isinstance(data["resources"], list):
        raise ValueError("'resources' must be a list")