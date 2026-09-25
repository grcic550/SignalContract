import pytest

from signalcontract.errors import SignalContractError, ValidationError
from signalcontract.models import Scenario
from signalcontract.scenario import load_scenario


def test_scenario_from_dict():
    """Test the from_dict method
    of the Scenario class."""

    valid_data = {
        "version": 1.0,
        "name": "Test Scenario",
        "request": {
            "method": "GET",
            "path": "/test",
        },
        "expected_status": 200,
        "contract": "test_contract.yaml",
    }

    assert Scenario.from_dict(valid_data) is not None
    assert Scenario.from_dict(valid_data).name == "Test Scenario"
    assert Scenario.from_dict(valid_data).request_method == "GET"
    assert Scenario.from_dict(valid_data).request_path == "/test"
    assert Scenario.from_dict(valid_data).expected_status == 200
    assert Scenario.from_dict(valid_data).contract_path == "test_contract.yaml"


def test_scenario_from_dict_invalid_data():
    """Test the from_dict method of the Scenario class
    with invalid data."""

    invalid_data = {
        "version": 1.0,
        "name": "Test Scenario",
        "request": {
            "method": "GET",
            "path": "/test",
        },
        # Missing expected_status and contract fields
    }

    with pytest.raises(
        ValidationError,
        match=r"Missing required scenario field expected_status.",
    ) as error:
        Scenario.from_dict(invalid_data)

    assert "Missing required scenario field expected_status." in str(error.value)


def test_scenario_from_dict_invalid_request():
    """Test the from_dict method of the Scenario class
    with invalid request data."""

    invalid_request_data = {
        "version": 1.0,
        "name": "Test Scenario",
        "request": {
            # Missing method and path fields
        },
        "expected_status": 200,
        "contract": "test_contract.yaml",
    }

    with pytest.raises(
        ValidationError,
        match=r"Scenario field request must not be empty.",
    ) as error:
        Scenario.from_dict(invalid_request_data)

    assert "Scenario field request must not be empty." in str(error.value)


def test_scenario_from_dict_data_not_dict_raises_ValidationError():
    """Test the from_dict method of Scenario class
    with data that is not a dictionary, expecting a ValidationError."""

    invalid_data = ["not", "a", "dict"]

    with pytest.raises(
        ValidationError,
        match=r"Scenario data must be a dictionary, but got <class 'list'>",
    ) as error:
        Scenario.from_dict(invalid_data)

    assert "Scenario data must be a dictionary, but got <class 'list'>" in str(
        error.value
    )


def test_scenario_from_dict_missing_required_fields_raises_ValidationError():
    """Test the from_dict method of Scenario class
    with data missing required fields, expecting a ValidationError"""

    invalid_data = {
        "version": 1.0,
        "name": "Test Scenario",
        # Missing 'request', 'expected_status', and 'contract' fields
    }

    with pytest.raises(
        ValidationError,
        match=r"Missing required scenario field request.",
    ) as error:
        Scenario.from_dict(invalid_data)

    assert "Missing required scenario field request." in str(error.value)


def test_scenario_from_dict_field_request_not_dict_raises_ValidationError():
    """Test the from_dict method of Scenario class
    with 'request' field not being a dictionary, expecting
     a ValidationError."""

    invalid_data = {
        "version": 1.0,
        "name": "Test Scenario",
        "request": "not a dict",  # Invalid request field
        "expected_status": 200,
        "contract": "test_contract.yaml",
    }

    with pytest.raises(
        ValidationError,
        match=r"Scenario request field must be a dictionary, but got <class 'str'>",
    ) as error:
        Scenario.from_dict(invalid_data)

    assert "Scenario request field must be a dictionary, but got <class 'str'>" in str(
        error.value
    )


def test_scenario_from_dict_empty_field_raises_ValidationError():
    """Test the from_dict method of Scenario class
    with empty required fields, expecting a ValidationError."""

    invalid_data = {
        "version": 1.0,
        "name": "",  # Empty name field
        "request": {
            "method": "GET",
            "path": "/test",
        },
        "expected_status": 200,
        "contract": "test_contract.yaml",
    }

    with pytest.raises(
        ValidationError,
        match=r"Scenario field name must not be empty.",
    ) as error:
        Scenario.from_dict(invalid_data)

    assert "Scenario field name must not be empty." in str(error.value)


def test_scenario_from_dict_request_field_without_method_or_path():
    """Test the from_dict method of Scenario class
    with 'request' field missing 'method' or 'path'
    raises ValidationError."""

    invalid_data_missing_method = {
        "version": 1.0,
        "name": "Test Scenario",
        "request": {
            # Missing 'method' field
            "path": "/test",
        },
        "expected_status": 200,
        "contract": "test_contract.yaml",
    }

    with pytest.raises(
        ValidationError,
        match=r"Missing required scenario request field 'method'.",
    ) as error:
        Scenario.from_dict(invalid_data_missing_method)

    assert "Missing required scenario request field 'method'." in str(error.value)

    invalid_data_missing_path = {
        "version": 1.0,
        "name": "Test Scenario",
        "request": {
            "method": "GET",
            # Missing 'path' field
        },
        "expected_status": 200,
        "contract": "test_contract.yaml",
    }

    with pytest.raises(
        ValidationError,
        match=r"Missing required scenario request field 'path'.",
    ) as error:
        Scenario.from_dict(invalid_data_missing_path)

    assert "Missing required scenario request field 'path'." in str(error.value)


def test_scenario_from_dict_invalid_version_raises_ValidationError():
    """Test the from_dict method of Scenario class
    with invalid 'version' field raises ValidationError."""

    invalid_data = {
        "version": True,  # Invalid version
        "name": "Test Scenario",
        "request": {
            "method": "GET",
            "path": "/test",
        },
        "expected_status": 200,
        "contract": "test_contract.yaml",
    }

    with pytest.raises(
        ValidationError,
        match=r"Scenario version must be an integer and equal to 1 "
        r"because only version 1 is supported.",
    ) as error:
        Scenario.from_dict(invalid_data)

    assert (
        "Scenario version must be an integer and equal to 1 "
        "because only version 1 is supported." in str(error.value)
    )


def test_scenario_from_dict_invalid_request_method_raises_ValidationError():
    """Test the from_dict method of Scenario class
    with invalid 'request method raises ValidationError."""

    invalid_data = {
        "version": 1.0,
        "name": "Test Scenario",
        "request": {
            "method": "INVALID_METHOD",  # Invalid request method
            "path": "/test",
        },
        "expected_status": 200,
        "contract": "test_contract.yaml",
    }

    with pytest.raises(
        ValidationError,
        match=r"Scenario request -> method must be "
        r"one of \['GET', 'POST', 'DELETE', 'PUT', 'PATCH', 'HEAD', 'OPTIONS'\], "
        r"but got INVALID_METHOD ",
    ) as error:
        Scenario.from_dict(invalid_data)

    assert (
        "Scenario request -> method must be "
        "one of ['GET', 'POST', 'DELETE', 'PUT', 'PATCH', 'HEAD', 'OPTIONS'], "
        "but got INVALID_METHOD " in str(error.value)
    )


def test_scenario_from_dict_invalid_request_path_raises_ValidationError():
    """Test the from_dict method of Scenario class
    with 'request' path being string but
    not starting with a forward slash raises ValidationError."""

    invalid_data = {
        "version": 1.0,
        "name": "Test Scenario",
        "request": {
            "method": "GET",
            "path": "test",  # Invalid request path (does not start with '/')
        },
        "expected_status": 200,
        "contract": "test_contract.yaml",
    }

    with pytest.raises(
        ValidationError,
        match=r"Scenario request -> path must start "
        r"with a forward slash '/', but got test",
    ) as error:
        Scenario.from_dict(invalid_data)

    assert (
        "Scenario request -> path must start with a forward slash '/', but got test"
        in str(error.value)
    )


def test_scenario_from_dict_invalid_path_type_raises_ValidationError():
    """Test the from_dict method of Scenario class
    with 'request' path being not a string raises ValidationError."""

    invalid_data = {
        "version": 1.0,
        "name": "Test Scenario",
        "request": {
            "method": "GET",
            "path": 123,  # Invalid request path (not a string)
        },
        "expected_status": 200,
        "contract": "test_contract.yaml",
    }

    with pytest.raises(
        ValidationError,
        match=r"Scenario request -> path must be a string, but got <class 'int'>",
    ) as error:
        Scenario.from_dict(invalid_data)

    assert "Scenario request -> path must be a string, but got <class 'int'>" in str(
        error.value
    )


def test_scenario_from_dict_invalid_expected_status_type_raises_ValidationError():
    """Test the from_dict method of Scenario class
    with 'expected_status' being not an integer
    raises ValidationError."""

    invalid_data = {
        "version": 1.0,
        "name": "Test Scenario",
        "request": {
            "method": "GET",
            "path": "/test",
        },
        "expected_status": True,  # Invalid expected_status (not an integer)
        "contract": "test_contract.yaml",
    }

    with pytest.raises(
        ValidationError,
        match=r"Scenario expected_status must be an "
        r"integer between 100 and 599, but got True",
    ) as error:
        Scenario.from_dict(invalid_data)

    assert (
        "Scenario expected_status must be an integer "
        "between 100 and 599, but got True" in str(error.value)
    )


def test_scenario_from_dict_invalid_expected_status_value_raises_ValidationError():
    """Test the from_dict method of Scenario class
    with 'expected_Status' being an integer but not in the range 100-599
    raises ValidationError."""

    invalid_data = {
        "version": 1.0,
        "name": "Test Scenario",
        "request": {
            "method": "GET",
            "path": "/test",
        },
        "expected_status": 99,  # Invalid expected_status (not in range 100-599)
        "contract": "test_contract.yaml",
    }

    with pytest.raises(
        ValidationError,
        match=r"Scenario expected_status must be an integer "
        r"between 100 and 599, but got 99",
    ) as error:
        Scenario.from_dict(invalid_data)

    assert (
        "Scenario expected_status must be an integer "
        "between 100 and 599, but got 99" in str(error.value)
    )


def test_load_scenario_with_non_string_filename_raises_TypeError():
    """Test the load_scenario function with a non-string filename,
    expecting a TypeError."""

    with pytest.raises(
        TypeError,
        match=r"Scenario filename must be a string.",
    ) as error:
        load_scenario(123)

    assert "Scenario filename must be a string." in str(error.value)


def test_load_scenario_with_nonexistent_file_raises_FileNotFoundError():
    """Test the load_scenario function with a non-exisstent file
    expecting a FileNotFoundError."""

    with pytest.raises(
        FileNotFoundError,
        match=r"Scenario file not found: nonexistent_file.yaml",
    ) as error:
        load_scenario("nonexistent_file.yaml")

    assert "Scenario file not found: nonexistent_file.yaml" in str(error.value)


def test_load_scenario_with_invalid_yaml_raises_ValueError(tmp_path):
    """Test the load_scenario function with an invalid YAML file,
    expecting a ValueError."""

    invalid_yaml_file = tmp_path / "invalid_scenario.yaml"
    invalid_yaml_file.write_text("invalid: [unbalanced brackets")

    with pytest.raises(
        ValueError,
        match=r"Error parsing scenario YAML file .*: while parsing a flow sequence",
    ) as error:
        load_scenario(str(invalid_yaml_file))

    assert "Error parsing scenario YAML file" in str(error.value)


def test_load_scenario_with_invalid_data_structure_raises_error(tmp_path):
    """Test the load_scenario function with a YAML
    file that does not contain a dictionary,
    expecting a SignalContractError."""

    invalid_data_file = tmp_path / "invalid_data_scenario.yaml"
    invalid_data_file.write_text("- item1\n- item2\n")

    with pytest.raises(
        SignalContractError,
        match=r"Scenario file .* must contain a YAML "
        r"mapping \(dictionary\) at the top level.",
    ) as error:
        load_scenario(str(invalid_data_file))

    assert "Scenario file" in str(
        error.value
    ) and "must contain a YAML mapping (dictionary) at the top level." in str(
        error.value
    )
