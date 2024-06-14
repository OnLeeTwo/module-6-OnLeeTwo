import pytest
from unittest.mock import patch
from services.animal import data_validation, add_animal_services, update_animal_services


@pytest.fixture
def mock_enclosures():
    with patch(
        "services.animal.enclosures",
        {"EN-123456": {"name": "Wild West", "type": "Outdoor", "animals": []}},
    ):
        yield


@pytest.fixture
def mock_animals():
    with patch(
        "services.animal.animals",
        {
            "A-123456": {
                "name": "Tiger",
                "species": "Panthera tigris",
                "familia": "Felidae",
                "age": 6,
                "gender": "male",
            }
        },
    ):
        yield


@pytest.mark.parametrize(
    "input_data, expected_errors",
    [
        ({}, {}),
        (
            {
                "name": "Tiger",
                "species": "Panthera tigris",
                "familia": "Felidae",
                "age": 5,
                "gender": "male",
            },
            {},
        ),
        ({"name": "T"}, {"name": "Name must be between 2 and 64 characters"}),
        (
            {"name": "Tiger", "species": "Panthera tigris", "familia": "F"},
            {"familia": "Familia must be between 2 and 64 characters"},
        ),
        (
            {
                "name": "Tiger",
                "species": "Panthera tigris",
                "familia": "Felidae",
                "age": -1,
                "gender": "male",
            },
            {"age": "Age must be a non-negative number"},
        ),
        (
            {
                "name": "Tiger",
                "species": "Panthera tigris",
                "familia": "Felidae",
                "age": 5,
                "gender": "non-binary",
            },
            {"gender": "Gender must be 'female' or 'male'"},
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
            {
                "name": "Tiger",
                "species": "Panthera tigris",
                "familia": "Felidae",
                "age": 5,
                "gender": "male",
                "enclosure_id": "EN-123456",
            },
            {"success": "Tiger is added to animal database"},
            201,
        ),
        (
            {
                "name": "T",
                "species": "Panthera tigris",
                "familia": "Felidae",
                "age": 5,
                "gender": "male",
                "enclosure_id": "E-123456",
            },
            {
                "error": "Invalid data",
                "details": {"name": "Name must be between 2 and 64 characters"},
            },
            400,
        ),
        (
            {
                "name": "Tiger",
                "species": "Panthera tigris",
                "familia": "Felidae",
                "age": 5,
                "gender": "male",
            },
            {"error": "Missing fields ['enclosure_id']"},
            400,
        ),
        (
            {
                "name": "Tiger",
                "species": "Panthera tigris",
                "familia": "Felidae",
                "age": 5,
                "gender": "male",
                "enclosure_id": "INVALID_ID",
            },
            {"error": "Enclosure ID is not found"},
            404,
        ),
    ],
)
def test_add_animal_services(
    mock_enclosures, input_data, expected_response, expected_status_code
):
    result = add_animal_services(input_data)
    assert result["response"] == expected_response
    assert result["status_code"] == expected_status_code


@pytest.mark.parametrize(
    "animal_id, input_data, expected_response, expected_status_code",
    [
        (
            "A-123456",
            {
                "name": "Tiger Updated",
                "species": "Panthera tigris",
                "familia": "Felidae",
                "age": 6,
                "gender": "male",
            },
            {"success": "Tiger Updated is updated"},
            201,
        ),
        (
            "A-123456",
            {
                "name": "T",
                "species": "Panthera tigris",
                "familia": "Felidae",
                "age": 5,
                "gender": "male",
                "enclosure_id": "E-123456",
            },
            {
                "error": "Invalid data",
                "details": {"name": "Name must be between 2 and 64 characters"},
            },
            400,
        ),
        (
            "A-123456",
            {
                "nama": "Tiger",
                "species": "Panthera tigris",
                "familia": "Felidae",
                "age": 6,
                "gender": "male",
            },
            {"error": "Invalid input: Non-allowed fields ['nama']"},
            400,
        ),
    ],
)
def test_update_animal_services(
    mock_animals, animal_id, input_data, expected_response, expected_status_code
):
    result = update_animal_services(animal_id, input_data)
    assert result["response"] == expected_response
    assert result["status_code"] == expected_status_code
