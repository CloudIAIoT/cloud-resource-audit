from cloud_audit.auditor import audit_resource, audit_inventory

def test_no_owner_resource():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "running",
    "monthly_cost": 100,
    "tags": {},
    "environment": "test"
    }

    findings = audit_resource(resource)

    assert findings == [
        {
            "resource_id": resource["id"],
            "rule": "MISSING_OWNER",
            "severity": "medium",
            "message": "Resource has no owner tag"
        }
    ]

def test_owner_valid():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "stopped",
    "monthly_cost": 0,
    "tags": {
        "owner": "data-team"
    },
    "environment": "test"
    }
    findings = audit_resource(resource)

    assert findings == []

def test_no_environment_resource():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "stopped",
    "monthly_cost": 0,
    "tags": {"owner": "data-team"}
    }

    findings = audit_resource(resource)

    assert findings == [
        {
            "resource_id": resource["id"],
            "rule": "MISSING_ENVIRONMENT",
            "severity": "medium",
            "message": "Resource has no environment defined"
        }
    ]

def test_no_owner_no_environment_resource():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "running",
    "monthly_cost": 100,
    "tags": {}
    }

    findings = audit_resource(resource)

    assert findings == [
        {
            "resource_id": resource["id"],
            "rule": "MISSING_OWNER",
            "severity": "medium",
            "message": "Resource has no owner tag"
        },
        {
            "resource_id": resource["id"],
            "rule": "MISSING_ENVIRONMENT",
            "severity": "medium",
            "message": "Resource has no environment defined"
        }
    ]

def test_vm_stopped_with_cost():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "stopped",
    "monthly_cost": 100,
    "tags": {
        "owner": "data-team"
    },
    "environment": "test"
    }
    findings = audit_resource(resource)

    assert findings == [
        {
            "resource_id": resource["id"],
            "rule": "STOPPED_VM_COST",
            "severity": "high",
            "message": "Stopped virtual machine has a positive monthly cost"
        }
    ]

def test_vm_stopped_without_cost():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "stopped",
    "monthly_cost": 0,
    "tags": {
        "owner": "data-team"
    },
    "environment": "test"
    }
    findings = audit_resource(resource)

    assert findings == []

def test_vm_running_with_cost():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "running",
    "monthly_cost": 100,
    "tags": {
        "owner": "data-team"
    },
    "environment": "test"
    }
    findings = audit_resource(resource)

    assert findings == []

def test_storage_account_cost():
    resource = {
    "id": "storage-prod-01",
    "type": "storage_account",
    "status": "active",
    "monthly_cost": 100,
    "tags": {
        "owner": "data-team"
    },
    "environment": "test"
    }
    findings = audit_resource(resource)

    assert findings == []

def test_production_without_criticaity():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "running",
    "monthly_cost": 100,
    "tags": {
        "owner": "data-team"
    },
    "environment": "production"
    }
    findings = audit_resource(resource)

    assert findings == [
        {
            "resource_id": resource["id"],
            "rule": "MISSING_PRODUCTION_TAG",
            "severity": "high",
            "message": "Production resource has no criticality tag"
        }
    ]

def test_production_with_criticaity():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "running",
    "monthly_cost": 100,
    "tags": {
        "owner": "data-team",
        "criticality": "high"
    },
    "environment": "production"
    }
    findings = audit_resource(resource)

    assert findings == []

def test_development_with_criticaity():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "running",
    "monthly_cost": 100,
    "tags": {
        "owner": "data-team"
    },
    "environment": "development"
    }
    findings = audit_resource(resource)

    assert findings == []

def test_no_environment_no_criticality():
    resource = {
    "id": "vm-01",
    "type": "virtual_machine",
    "status": "running",
    "monthly_cost": 100,
    "tags": {
        "owner": "data-team"
    }
    }
    findings = audit_resource(resource)

    assert findings == [
        {
            "resource_id": resource["id"],
            "rule": "MISSING_ENVIRONMENT",
            "severity": "medium",
            "message": "Resource has no environment defined"
        }
    ]

def test_audit_empty_inventory():
    data = {
        "inventory_version": "1.0",
        "resources": []
    }

    findings = audit_inventory(data)

    assert findings == []

def test_audit_inventory_no_findings():
    data = {
        "inventory_version": "1.0",
        "resources": [
            {
                "id": "vm-prod-01",
                "type": "virtual_machine",
                "status": "running",
                "monthly_cost": 125.50,
                "tags": {
                    "owner": "platform-team",
                    "criticality": "high"
                },
                "environment": "production"
            },
            {
                "id": "storage-dev-01",
                "type": "storage_account",
                "status": "active",
                "monthly_cost": 18.75,
                "tags": {
                    "owner": "development-team"
                },
                "environment": "development"
            }
        ]
    }
    findings = audit_inventory(data)

    assert findings == []

def test_audit_inventory_multiple_findings():
    data = {
        "inventory_version": "1.0",
        "resources": [
            {
                "id": "vm-test-01",
                "type": "virtual_machine",
                "status": "stopped",
                "monthly_cost": 42.00,
                "tags": {},
                "environment": "test"
            },
            {
                "id": "storage-prod-01",
                "type": "storage_account",
                "status": "active",
                "monthly_cost": 18.75,
                "tags": {
                    "owner": "data-team"
                },
                "environment": "production"
            },
            {
                "id": "vm-dev-01",
                "type": "virtual_machine",
                "status": "running",
                "monthly_cost": 80.00,
                "tags": {}
            }
        ]
    }
    findings = audit_inventory(data)
    assert findings == [
        {
            "resource_id": "vm-test-01",
            "rule": "MISSING_OWNER",
            "severity": "medium",
            "message": "Resource has no owner tag"
        },
        {
            "resource_id": "vm-test-01",
            "rule": "STOPPED_VM_COST",
            "severity": "high",
            "message": "Stopped virtual machine has a positive monthly cost"
        },
        {
            "resource_id": "storage-prod-01",
            "rule": "MISSING_PRODUCTION_TAG",
            "severity": "high",
            "message": "Production resource has no criticality tag"
        },
        {
            "resource_id": "vm-dev-01",
            "rule": "MISSING_OWNER",
            "severity": "medium",
            "message": "Resource has no owner tag"
        },
        {
            "resource_id": "vm-dev-01",
            "rule": "MISSING_ENVIRONMENT",
            "severity": "medium",
            "message": "Resource has no environment defined"
        }
    ]
