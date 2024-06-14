import pytest
from unittest.mock import patch
from services.enclosure import (
    data_validation,
    add_enclosure_services,
    update_enclosure_services,
    delete_enclosure_services,
)


@pytest.fixture
def mock_enclosures():
    with patch(
        "services.enclosure.enclosures",
        {
            "EN-123ENC": {"name": "Wild West", "type": "Outdoor", "animals": []},
            "EN-ENC456": {
                "name": "Wild West",
                "type": "Outdoor",
                "animals": ["A-123ABC", "A-BCA123"],
            },
        },
    ):
        yield


@pytest.mark.parametrize(
    "input_data, expected_errors",
    [
        ({}, {}),
        (
            {"name": "Forest", "type": "Outdoor"},
            {},
        ),
        (
            {"name": "F", "type": "Outdoor"},
            {"name": "Name must be between 2 and 64 characters"},
        ),
        (
            {"name": "Forest", "type": "O"},
            {"type": "Type must be between 2 and 64 characters"},
        ),
    ],
)
def test_data_validation(input_data, expected_errors):
    errors = data_validation(input_data)
    assert errors == expected_errors


@pytest.mark.parametrize(
    "input_data, expected_response, expected_status_code",
    [
        (
            {"name": "Forest", "type": "Outdoor"},
            {"success": "Forest is added to enclosure database"},
            201,
        ),
        (
            {"name": "F", "type": "Outdoor"},
            {
                "error": "Invalid data",
                "details": {"name": "Name must be between 2 and 64 characters"},
            },
            400,
        ),
        (
            {"name": "Forest"},
            {"error": "Missing fields ['type']"},
            400,
        ),
    ],
)
def test_add_enclosure_services(
    mock_enclosures, input_data, expected_response, expected_status_code
):
    result = add_enclosure_services(input_data)
    assert result["response"] == expected_response
    assert result["status_code"] == expected_status_code


@pytest.mark.parametrize(
    "enclosure_id, input_data, expected_response, expected_status_code",
    [
        (
            "EN-123ENC",
            {"name": "Forest", "type": "Outdoor"},
            {"success": "Forest is updated"},
            201,
        ),
        (
            "EN-123ENC",
            {"name": "F", "type": "Outdoor"},
            {
                "error": "Invalid data",
                "details": {"name": "Name must be between 2 and 64 characters"},
            },
            400,
        ),
        (
            "EN-123ENC",
            {"nama": "Forest", "type": "Outdoor"},
            {"error": "Invalid input: Non-allowed fields ['nama']"},
            400,
        ),
    ],
)
def test_update_enclosure_services(
    mock_enclosures, enclosure_id, input_data, expected_response, expected_status_code
):
    result = update_enclosure_services(enclosure_id, input_data)
    assert result["response"] == expected_response
    assert result["status_code"] == expected_status_code


@pytest.mark.parametrize(
    "enclosure_id, expected_response, expected_status_code",
    [
        (
            "EN-123ENC",
            {"success": "Enclosure with ID EN-123ENC is deleted"},
            200,
        ),
        (
            "EN-ENC456",
            {"error": "Enclosure is not empty, relocate the animal inhabiting first!"},
            400,
        ),
    ],
)
def test_delete_enclosure_services(
    mock_enclosures, enclosure_id, expected_response, expected_status_code
):
    result = delete_enclosure_services(enclosure_id)
    assert result["response"] == expected_response
    assert result["status_code"] == expected_status_code
