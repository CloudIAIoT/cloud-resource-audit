



def audit_resource(resource):

    findings = []

    if "owner" not in resource["tags"]:
        findings.append({
            "resource_id": resource["id"],
            "rule": "MISSING_OWNER",
            "severity": "medium",
            "message": "Resource has no owner tag"
        })

    if "environment" not in resource:
        findings.append({
            "resource_id": resource["id"],
            "rule": "MISSING_ENVIRONMENT",
            "severity": "medium",
            "message": "Resource has no environment defined"
        })

    if resource["type"] == "virtual_machine" and resource["status"] == "stopped" and resource["monthly_cost"] > 0:
        findings.append({
            "resource_id": resource["id"],
            "rule": "STOPPED_VM_COST",
            "severity": "high",
            "message": "Stopped virtual machine has a positive monthly cost"
        })

    if resource.get("environment") == "production" and "criticality" not in resource["tags"]:
        findings.append({
            "resource_id": resource["id"],
            "rule": "MISSING_PRODUCTION_TAG",
            "severity": "high",
            "message": "Production resource has no criticality tag"
        })

    return findings
    



def audit_inventory(data):
    findings = []

    for resource in data["resources"]:
        findings_resource = audit_resource(resource)
        findings.extend(findings_resource)

    return findings

