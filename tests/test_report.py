from cloud_audit.report import format_report
from cloud_audit.auditor import audit_inventory
from cloud_audit.statistics import calculate_statistics

def test_report_with_findings():
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
    report = format_report(statistics, findings)

    assert "INVENTORY SUMMARY" in report
    assert "Total resources: 3" in report
    assert "Virtual machines: 2" in report
    assert "Storage accounts: 1" in report
    assert "Total monthly cost: $140.75" in report
    assert "AUDIT SUMMARY" in report
    assert "Total findings: 5" in report
    assert "High severity: 2" in report
    assert "Medium severity: 3" in report
    assert "FINDINGS" in report
    assert "[HIGH] vm-test-01" in report
    assert "Rule: STOPPED_VM_COST" in report


def test_report_without_findings():
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
    report = format_report(statistics, findings)

    assert "No findings detected." in report
    assert "INVENTORY SUMMARY" in report
    assert "Total resources: 2" in report
    assert "Virtual machines: 1" in report
    assert "Storage accounts: 1" in report
    assert "Total monthly cost: $144.25" in report