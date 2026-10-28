
def calculate_statistics(inventory, findings):

    total_monthly_cost = 0

    statistics = {
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
    for resource in inventory["resources"]:
        statistics["resources_by_type"][resource["type"]] = statistics["resources_by_type"].get(resource["type"], 0) + 1
        total_monthly_cost += resource["monthly_cost"]

    for finding in findings:
        statistics["findings_by_severity"][finding["severity"]] = statistics["findings_by_severity"].get(finding["severity"], 0) + 1

    statistics["total_resources"] = len(inventory["resources"])
    statistics["total_monthly_cost"] = total_monthly_cost
    statistics["total_findings"] = len(findings)
    
    return statistics

