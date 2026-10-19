from cloud_audit.loader import load_resources
import json
import pytest

def test_load_dict(tmp_path):

    file_path = tmp_path / "test.json"

    data_1 = {
        "name": "test",
        "value": 100
    }

    file_path.write_text(json.dumps(data_1))

    result_1 = load_resources(file_path)

    assert result_1 == data_1


def test_load_list(tmp_path):

    file_path = tmp_path / "test.json"
    data_2 = [10, 20, 30]

    file_path.write_text(json.dumps(data_2))

    result_2 = load_resources(file_path)

    assert result_2 == data_2



def test_file_not_found(tmp_path):
    file_path = tmp_path / "nonexistent.json"

    with pytest.raises(FileNotFoundError):
        load_resources(file_path)

def test_malformed_json(tmp_path):
    file_path = tmp_path / "malformed.json"

    file_path.write_text('{"name": "test", "value": }')

    with pytest.raises(json.JSONDecodeError):
        load_resources(file_path)