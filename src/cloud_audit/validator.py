import math

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

    for resource in data["resources"]:
        validate_resource(resource)


def validate_resource(resource):

    if not isinstance(resource, dict):
        raise ValueError("Resource must be a Python dictionary")

    required_resource_keys = {"id", "type", "status", "monthly_cost", "tags"}
    missing_keys = required_resource_keys - resource.keys()
    if missing_keys:
        raise ValueError(f"The following keys are missing: {missing_keys}")

    if not isinstance(resource["id"], str) or resource["id"].strip() == "":
        raise TypeError('"id" must be a non empty Python string')

    if not isinstance(resource["type"], str):
        raise TypeError('"type" must be a Python string')

    allowed_resources = {"virtual_machine", "storage_account"}
    if resource["type"] not in allowed_resources:
        raise ValueError(f"{resource['type']} is not a supported resource")

    if not isinstance(resource["status"], str):
        raise TypeError('"status" must be a Python string')

    allowed_status = {
        "virtual_machine": {"running", "stopped"},
        "storage_account": {"active"}
    }
    if resource["status"] not in allowed_status[resource["type"]]:
        raise ValueError(f"Status: {resource['status']} is unsupported for {resource["type"]}")       

    if not isinstance(resource["monthly_cost"], (int, float)) or isinstance(resource["monthly_cost"], bool):
        raise TypeError('"monthly_cost" must be a number (integer or float)')

    if resource["monthly_cost"] < 0:
        raise ValueError("The cost can't be negative")

    if not math.isfinite(resource["monthly_cost"]):
        raise ValueError("Cost must be a defined finite value")

    if not isinstance(resource["tags"], dict):
        raise TypeError('"tags" must be a Pythion dictionary')

    for key, value in resource["tags"].items():
        if not isinstance (key, str):
            raise TypeError("keys must contain only strings")
        if not isinstance(value, str):
            raise TypeError("values must contain only strings")
        if key == "owner" and value.strip() == "":
            raise ValueError('The value of "owner" must be a non empty string')

    if "environment" in resource:
        allowed_values = {"production", "development", "test"}
        if resource["environment"] not in allowed_values:
            raise ValueError ("The environment is invalid")
        