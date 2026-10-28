from cloud_audit.auditor import audit_inventory
from cloud_audit.statistics import calculate_statistics

def format_report(statistics, findings):
    report = f"""
INVENTORY SUMMARY
Total resources: {statistics['total_resources']}
Virtual machines: {statistics["resources_by_type"]["virtual_machine"]}
Storage accounts: {statistics["resources_by_type"]["storage_account"]}
Total monthly cost: ${statistics["total_monthly_cost"]:.2f}

AUDIT SUMMARY
Total findings: {statistics["total_findings"]}
High severity: {statistics["findings_by_severity"]["high"]}
Medium severity: {statistics["findings_by_severity"]["medium"]}
Low severity: {statistics["findings_by_severity"]["low"]}

FINDINGS
        """

    if findings == []:
        report += """
No findings detected. """

    else:

        for finding in findings:
            report += f"""
[{finding["severity"].upper()}] {finding["resource_id"]}
Rule: {finding["rule"]}
{finding["message"]}
        """

    return report

