import sys
import pytest
from cloud_audit.cli import main


def test_cli_valid_inventory(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["cloud-audit", "data/inventory_clean.json"]
    )

    main()

    captured = capsys.readouterr()

    assert "INVENTORY SUMMARY" in captured.out
    assert "Total resources: 5" in captured.out
    assert "No findings detected." in captured.out


def test_cli_file_not_found(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["cloud-audit", "data/inventory_inexistent.json"]
    )


    with pytest.raises(SystemExit) as exc_info:
        main()

    captured = capsys.readouterr()

    assert exc_info.value.code == 1
    assert "Error: Inventory file not found." in captured.err
    assert captured.out == ""

def test_cli_invald_json(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["cloud-audit", "data/inventory_invalid_file.json"]
    )


    with pytest.raises(SystemExit) as exc_info:
        main()

    captured = capsys.readouterr()

    assert exc_info.value.code == 1
    assert "Error: Invalid JSON format." in captured.err
    assert captured.out == ""

def test_cli_invald_inventory(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["cloud-audit", "data/invalid_inventory.json"]
    )


    with pytest.raises(SystemExit) as exc_info:
        main()

    captured = capsys.readouterr()

    assert exc_info.value.code == 1
    assert "Error: Invalid inventory data." in captured.err
    assert captured.out == ""