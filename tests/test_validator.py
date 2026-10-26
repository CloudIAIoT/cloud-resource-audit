from cloud_audit.validator import validate_inventory, validate_resource
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
        "resources": {}
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

def test_valid_resource():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "running", 
    "monthly_cost": 100,
    "tags": {}
    }
    validate_resource(resource)

def test_list_resource():
    resource = ["id", "type", "status", "monthly_cost", "tags"]
    with pytest.raises(ValueError, match="Resource must be a Python dictionary"):
        validate_resource(resource)

def test_missing_key_tags():
    resource = {
    "id": "vm-02",
    "type": "virtual_machine",
    "status": "running",
    "monthly_cost": 100
    }
    with pytest.raises(ValueError, match="tags"):
        validate_resource(resource)

def test_id_key():
    resource = {
    "id": 2,
    "type": "virtual_machine",
    "status": "running",
    "monthly_cost": 100,
    "tags": {}
    }
    with pytest.raises(TypeError, match="id"):
        validate_resource(resource)

def test_type_key():
    resource = {
    "id": "vm-02",
    "type": 8,
    "status": "running",
    "monthly_cost": 100,
    "tags": {}
    }
    with pytest.raises(TypeError, match="type"):
        validate_resource(resource)

def test_status_key():
    resource = {
    "id": "vm-02",
    "type": "virtual_machine",
    "status": 5,
    "monthly_cost": 100,
    "tags": {}
    }
    with pytest.raises(TypeError, match="status"):
        validate_resource(resource)

def test_monthly_cost_key():
    resource = {
    "id": "vm-02",
    "type": "virtual_machine",
    "status": "stopped",
    "monthly_cost": True,
    "tags": {}
    }
    with pytest.raises(TypeError, match="monthly_cost"):
        validate_resource(resource)

def test_tags_key():
    resource = {
    "id": "vm-02",
    "type": "virtual_machine",
    "status": "stopped",
    "monthly_cost": 100,
    "tags": []
    }
    with pytest.raises(TypeError, match="tags"):
        validate_resource(resource)

def test_empty_id():
    resource = {
    "id": "",
    "type": "virtual_machine",
    "status": "running",
    "monthly_cost": 100,
    "tags": {}
    }
    with pytest.raises(TypeError, match="id"):
        validate_resource(resource)

def test_whitespace_id():
    resource = {
    "id": "   ",
    "type": "virtual_machine",
    "status": "running",
    "monthly_cost": 100,
    "tags": {}
    }
    with pytest.raises(TypeError, match="id"):
        validate_resource(resource)

def test_valid_virtual_machine_type():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "running",
    "monthly_cost": 100,
    "tags": {}
    }
    validate_resource(resource)

def test_valid_storage_account_type():
    resource = {
    "id": "vm-01",
    "type": "storage_account",
    "status": "active",
    "monthly_cost": 100,
    "tags": {}
    }
    validate_resource(resource)

def test_unsupported_resource_type():
    resource = {
    "id": "vm-01",
    "type": "data_base",
    "status": "running",
    "monthly_cost": 100,
    "tags": {}
    }
    with pytest.raises(ValueError, match="supported resource"):
        validate_resource(resource)

def test_virtual_machine_valid_status():
    resource_running = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "running",
    "monthly_cost": 100,
    "tags": {}
    }
    validate_resource(resource_running)
    resource_stopped = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "stopped",
    "monthly_cost": 100,
    "tags": {}
    }
    validate_resource(resource_stopped)

def test_storage_account_valid_status():
    resource = {
    "id": "vm-01",
    "type": "storage_account",
    "status": "active",
    "monthly_cost": 100,
    "tags": {}
    }
    validate_resource(resource)

def test_storage_account_running():
    resource = {
    "id": "vm-01",
    "type": "storage_account",
    "status": "running",
    "monthly_cost": 100,
    "tags": {}
    }
    with pytest.raises(ValueError, match="is unsupported for"):
        validate_resource(resource)

def test_negative_cost():
    resource = {
    "id": "vm-01",
    "type": "storage_account",
    "status": "active",
    "monthly_cost": -100,
    "tags": {}
    }
    with pytest.raises(ValueError, match="negative"):
        validate_resource(resource)

def test_positive_cost():
    resource = {
    "id": "vm-01",
    "type": "storage_account",
    "status": "active",
    "monthly_cost": 125.50,
    "tags": {}
    }
    validate_resource(resource)

def test_zero_cost():
    resource = {
    "id": "vm-01",
    "type": "storage_account",
    "status": "active",
    "monthly_cost": 0,
    "tags": {}
    }
    validate_resource(resource)

def test_infinite_cost():
    resource = {
    "id": "vm-01",
    "type": "storage_account",
    "status": "active",
    "monthly_cost": float("inf"),
    "tags": {}
    }
    with pytest.raises(ValueError, match="finite"):
        validate_resource(resource)

def test_nan_cost():
    resource = {
    "id": "vm-01",
    "type": "storage_account",
    "status": "active",
    "monthly_cost": float("nan"),
    "tags": {}
    }
    with pytest.raises(ValueError, match="defined"):
        validate_resource(resource)

def test_empty_tags():
    resource = {
    "id": "vm-01",
    "type": "storage_account",
    "status": "active",
    "monthly_cost": 100,
    "tags": {}
    }
    validate_resource(resource)

def test_invalid_tag_key():
    resource = {
    "id": "vm-01",
    "type": "storage_account",
    "status": "active",
    "monthly_cost": 100,
    "tags": {10: "team"}
    }
    with pytest.raises(TypeError, match="keys"):
        validate_resource(resource)

def test_invalid_tag_value():
    resource = {
    "id": "vm-01",
    "type": "storage_account",
    "status": "active",
    "monthly_cost": 100,
    "tags": {"owner": 123}
    }
    with pytest.raises(TypeError, match="values"):
        validate_resource(resource)

def test_invalid_empty_owner():
    resource = {
    "id": "vm-01",
    "type": "storage_account",
    "status": "active",
    "monthly_cost": 100,
    "tags": {"owner": "   "}
    }
    with pytest.raises(ValueError, match="empty string"):
        validate_resource(resource)

def test_no_environment():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "stopped",
    "monthly_cost": 100,
    "tags": {"8": "name",
             "owner": " f  "}
    }
    validate_resource(resource)

def test_environment_production():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "stopped",
    "monthly_cost": 100,
    "tags": {"8": "name",
             "owner": " f  "},
    "environment": "production"
    }
    validate_resource(resource)

def test_environment_invalid():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "stopped",
    "monthly_cost": 100,
    "tags": {"8": "name",
             "owner": " f  "},
    "environment": "staging"
    }
    with pytest.raises(ValueError, match='environment'):
        validate_resource(resource)

def test_environment_none():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "stopped",
    "monthly_cost": 100,
    "tags": {"8": "name",
             "owner": " f  "},
    "environment": None
    }
    with pytest.raises(ValueError, match="environment"):
        validate_resource(resource)

def test_invenotry_empty_resources():
    data = {
        "inventory_version": "1.0",
        "resources": []
    }
    validate_inventory(data)

def test_inventory_valid_resources():
    data = {
        "inventory_version": "1.0",
        "resources": [
            {
                "id": "vm-01",
                "type": "virtual_machine",
                "status": "stopped",
                "monthly_cost": 42.75,
                "tags": {"owner": "patform-team"}
            },
            {
                "id": "storage-prod-01",
                "type": "storage_account",
                "status": "active",
                "monthly_cost": 18.75,
                "tags": {
                    "criticaly": "medium"
                },
                "environment": "production"
            }
        ]
    }
    validate_inventory(data)

def test_inventory_invalid_resource():
    data = {
        "inventory_version": "1.0",
        "resources": [
            {
                "id": "vm-01",
                "type": "virtual_machine",
                "status": "active",
                "monthly_cost": 100,
                "tags": {},
                "environment": "test"
            }
        ]
    }
    with pytest.raises(ValueError, match="Status"):
        validate_inventory(data)

def test_inventory_invalid_second_resource():
    data = {
        "inventory_version": "1.0",
        "resources": [
            {
            "id": "vm-01",
            "type": "virtual_machine",
            "status": "stopped",
            "monthly_cost": 42.75,
            "tags": {"owner": "patform-team"}
            },
            {
                "id": "vm-01",
                "type": "virtual_machine",
                "status": "stopped",
                "monthly_cost": 100,
                "tags": {},
                "environment": "developers"
            }
        ]
    }
    with pytest.raises(ValueError, match="environment"):
        validate_inventory(data)