from cloud_audit.statistics import calculate_statistics
from cloud_audit.auditor import audit_inventory

def test_statistics_empty_inventory():
    data = {
        "inventory_version": "1.0",
        "resources": []
    }

    findings = audit_inventory(data)
    statistics = calculate_statistics(data, findings)
    assert statistics == {
        "total_resources": 0,
        "resources_by_type": {
            "virtual_machine": 0,
            "storage_account": 0
        },
        "total_monthly_cost": 0,
        "total_findings": 0,
        "findings_by_severity": {
            "high": 0,
            "medium": 0,
            "low": 0
        }
    }

def test_multiple_resources():
    
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
    statistics = calculate_statistics(data, findings)

    assert statistics == {
        'total_resources': 3, 
        'resources_by_type': {
            'virtual_machine': 2, 
            'storage_account': 1
            }, 
        'total_monthly_cost': 140.75, 
        'total_findings': 5,
        'findings_by_severity': {
            'high': 2, 
            'medium': 3, 
            'low': 0
            }
        }

def test_multiple_resources_no_findings():
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
    statistics = calculate_statistics(data, findings)
    assert statistics == {
        'total_resources': 2, 
        'resources_by_type': {
            'virtual_machine': 1, 
            'storage_account': 1
            }, 
        'total_monthly_cost': 144.25, 
        'total_findings': 0, 
        'findings_by_severity': {
            'high': 0, 
            'medium': 0, 
            'low': 0
            }
        }
