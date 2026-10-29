# Cloud Resource Audit CLI

A Python command-line tool for auditing simulated cloud resource inventories, detecting configuration issues, and generating structured reports.

## Overview

Cloud Resource Audit CLI is a lightweight Python application designed to analyze cloud infrastructure inventories stored in JSON files.

The application validates resource data, applies predefined auditing rules, calculates inventory statistics, and produces a human-readable report directly in the terminal.

The project demonstrates practical software engineering skills, including modular Python development, input validation, exception handling, automated testing, and command-line application packaging.

**Current scope:** The application uses simulated cloud resource inventories. It does not connect to Azure or other cloud providers.

## Features

- Load cloud resource inventories from JSON files.
- Validate inventory structure and resource attributes.
- Detect configuration and cost-related issues.
- Classify audit findings by severity.
- Calculate resource counts and estimated monthly costs.
- Generate readable terminal reports.
- Handle invalid files and inventory data with clear error messages.
- Execute audits using the `cloud-audit` command.
- Run automated tests with pytest.

## Technology Stack

- **Python 3.12+** — Application development
- **Python Standard Library** — JSON processing, argument parsing, and error handling
- **pytest** — Automated testing
- **setuptools** — Python package configuration and installation
- **Git and GitHub** — Version control

## Project Structure

```text
cloud-resource-audit/
├── data/                     # Sample JSON inventories
├── src/
│   └── cloud_audit/
│       ├── loader.py         # JSON file loading
│       ├── validator.py      # Inventory validation
│       ├── auditor.py        # Audit rules
│       ├── statistics.py     # Inventory statistics
│       ├── report.py         # Report formatting
│       └── cli.py            # Command-line interface
├── tests/                    # Automated tests
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone git@github.com:CloudIAIoT/cloud-resource-audit.git
cd cloud-resource-audit
```

Alternatively, clone the repository using HTTPS:

```bash
git clone https://github.com/CloudIAIoT/cloud-resource-audit.git
```

### 2. Create a virtual environment

On Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the project

```bash
python -m pip install -e .
```

The editable installation registers the `cloud-audit` command.

## Usage

Run an audit by providing the path to a JSON inventory:

```bash
cloud-audit data/inventory_clean.json
```

To analyze an inventory containing configuration issues:

```bash
cloud-audit data/inventory_findings.json
```

Display command-line help:

```bash
cloud-audit --help
```

## Supported Resource Types

| Resource Type | Supported Statuses |
|---|---|
| `virtual_machine` | `running`, `stopped` |
| `storage_account` | `active` |

Each resource requires an ID, type, status, monthly cost, and tags dictionary.

The `environment` field is optional. Missing environment information is reported as an audit finding rather than treated as an invalid inventory.

Supported environments are `production`, `development`, and `test`.

## Audit Rules

The application implements four auditing rules:

| Rule | Severity | Description |
|---|---|---|
| `MISSING_OWNER` | Medium | A resource does not have an owner tag. |
| `MISSING_ENVIRONMENT` | Medium | A resource does not define an environment. |
| `STOPPED_VM_COST` | High | A stopped virtual machine has a positive monthly cost. |
| `MISSING_PRODUCTION_TAG` | High | A production resource does not have a criticality tag. |

A single resource can trigger multiple findings.

## Example Output

The following example illustrates a report for an inventory containing configuration issues:

```text
INVENTORY SUMMARY
Total resources: 3
Virtual machines: 2
Storage accounts: 1
Total monthly cost: $140.75

AUDIT SUMMARY
Total findings: 5
High severity: 2
Medium severity: 3
Low severity: 0

FINDINGS

[MEDIUM] vm-test-01
Rule: MISSING_OWNER
Resource has no owner tag

[HIGH] vm-test-01
Rule: STOPPED_VM_COST
Stopped virtual machine has a positive monthly cost
```

Additional findings are displayed using the same format.

Monthly costs are provided by the input inventory. The application does not retrieve actual cloud billing data.

## Error Handling

The CLI handles common input errors, including:

- Missing inventory files.
- Malformed JSON.
- Invalid inventory structure.
- Missing required resource attributes.
- Unsupported resource types or statuses.
- Invalid monthly cost values.

The application returns exit code `0` after a successful audit, including audits that detect findings.

Input errors return exit code `1`.

## Automated Testing

The project uses pytest to verify inventory loading, validation, auditing, statistics, and report generation.

Install pytest if it is not already available:

```bash
python -m pip install pytest
```

Run the automated tests from the repository root:

```bash
python -m pytest -v
```

## Current Limitations

- Inventories must be supplied as local JSON files.
- Resource types and audit rules are predefined.
- Monthly costs are estimates provided in the inventory.
- The application does not connect to live cloud infrastructure.
- Reports are displayed in the terminal rather than exported to files.

## Future Improvements

Potential extensions include:

- Integration with Azure resource inventories.
- Additional audit rules for security, governance, and cost optimization.
- Configurable audit policies.
- JSON or CSV report export.
- Automated execution in CI/CD workflows.

## License

No license has been specified for this project.
