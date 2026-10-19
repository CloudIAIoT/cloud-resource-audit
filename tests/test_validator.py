from cloud_audit.validator import validate_inventory
import pytest

def test_correct_input():
    data = {
        "inventory_version": "1.0",
        "resources": []
    }
    validate_inventory(data)

def test_data_is_list():
    data = []
    with pytest.raises(ValueError, match="The inventory must be a Python dictionary"):
        validate_inventory(data)

def test_no_inventory_version():
    data = {
        "resources": []
    }
    with pytest.raises(ValueError, match="inventory_version"):
        validate_inventory(data)

def test_no_resources():
    data = {
        "inventory_version": "1.0"
    }
    with pytest.raises(ValueError, match="resources"):
        validate_inventory(data)

def test_invalid_inventory_version():
    data = {
        "inventory_version": "2.0",
        "resources": []
    }
    with pytest.raises(ValueError, match="Unsupported inventory version"):
        validate_inventory(data)

def test_invalid_resources_format():
    data = {
        "inventory_version": "1.0",
        "resources": "my_resources"
    }
    with pytest.raises(ValueError, match="'resources' must be a list"):
        validate_inventory(data)