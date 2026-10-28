import argparse
import sys
import json
from cloud_audit.loader import load_resources
from cloud_audit.validator import validate_inventory
from cloud_audit.auditor import audit_inventory
from cloud_audit.statistics import calculate_statistics
from cloud_audit.report import format_report

def main():
    parser = argparse.ArgumentParser(
        description="Cloud Resource Audit CLI application"
    )

    parser.add_argument(
        "filename",
        help="Path to the input file"
    )

    args = parser.parse_args()

    try:
        data = load_resources(args.filename)
        validate_inventory(data)
        print("Inventory loaded and validated successfully.")
        findings = audit_inventory(data)
        statistics = calculate_statistics(data, findings)
        report = format_report(statistics, findings)
        print(report)        

    except FileNotFoundError:
        print("Error: Inventory file not found.", file=sys.stderr)
        sys.exit(1)

    except json.JSONDecodeError:
        print("Error: Invalid JSON format.", file=sys.stderr)
        sys.exit(1)

    except ValueError as error:
        print(f"Error: Invalid inventory data. {error}", file=sys.stderr)
        sys.exit(1)

    except TypeError as error:
        print(f"Error: Invalid inventory data. {error}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
