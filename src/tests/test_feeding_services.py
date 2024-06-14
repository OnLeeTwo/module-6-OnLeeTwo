import pytest
from unittest.mock import patch
from services.feeding import (
    data_validation,
    add_feeding_services,
    update_feeding_services,
    delete_feeding_services,
)

mocked_employees = {
    "E-123456": {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "+62234567890",
        "role": "Zoo Keeper",
        "schedule": ["F-123FEE"],
    },
    "E-456DEF": {
        "name": "Alice Smith",
        "email": "alice.smith@example.com",
        "phone": "+62987654321",
        "role": "Zoo Keeper",
        "schedule": [],
    },
}

mocked_animals = {
    "A-123456": {
        "name": "Tiger",
        "species": "Panthera tigris",
        "familia": "Felidae",
        "age": 6,
        "gender": "male",
    },
    "A-135792": {
        "name": "Leo",
        "species": "Lion",
        "familia": "Felidae",
        "age": 5,
        "gender": "Male",
    },
}


@pytest.fixture
def mock_employees():
    with patch("services.feeding.employees", mocked_employees):
        yield


@pytest.fixture
def mock_animals():
    with patch("services.feeding.animals", mocked_animals):
        yield


@pytest.fixture
def mock_feedings():
    with patch(
        "services.feeding.feedings",
        {
            "F-123FEE": {
                "animal_id": "A-123456",
                "employee_id": "E-123456",
                "food_type": "Rabbit meat",
                "date": "17-06-2024",
                "time": "14.30",
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
                "animal_id": "A-135792",
                "employee_id": "E-456DEF",
                "food_type": "Chicken Meat",
                "date": "18-06-2024",
                "time": "11.00",
            },
            {},
        ),
        (
            {
                "animal_id": "INVALID_ID",
                "employee_id": "E-456DEF",
                "food_type": "Chicken Meat",
                "date": "18-06-2024",
                "time": "11.00",
            },
            {"animal_id": "Animal ID not found"},
        ),
        (
            {
                "animal_id": "A-135792",
                "employee_id": "iNVALID_ID",
                "food_type": "Chicken Meat",
                "date": "18-06-2024",
                "time": "11.00",
            },
            {"employee_id": "Employee ID not found"},
        ),
        (
            {
                "animal_id": "A-135792",
                "employee_id": "E-456DEF",
                "food_type": "C",
                "date": "18-06-2024",
                "time": "11.00",
            },
            {"food_type": "Food type must be between 2 and 64 characters"},
        ),
        (
            {
                "animal_id": "A-135792",
                "employee_id": "E-456DEF",
                "food_type": "Chicken Meat",
                "date": "2024-18-03",
                "time": "11.00",
            },
            {"date": "Date must be in the format 'dd-mm-yyyy'"},
        ),
        (
            {
                "animal_id": "A-135792",
                "employee_id": "E-456DEF",
                "food_type": "Chicken Meat",
                "date": "18-03-2024",
                "time": "2AM",
            },
            {"time": "Time must be in the format 'HH.MM'"},
        ),
    ],
)
def test_data_validation(mock_animals, mock_employees, input_data, expected_errors):
    errors = data_validation(input_data)
    assert errors == expected_errors


@pytest.mark.parametrize(
    "input_data, expected_response, expected_status_code",
    [
        (
            {
                "animal_id": "A-135792",
                "employee_id": "E-456DEF",
                "food_type": "Chicken Meat",
                "date": "18-06-2024",
                "time": "11.00",
            },
            {"success": "New schedule is added to feeding schedule database"},
            201,
        ),
        (
            {
                "animal_id": "INVALID_ID",
                "employee_id": "E-456DEF",
                "food_type": "Chicken Meat",
                "date": "18-06-2024",
                "time": "11.00",
            },
            {
                "error": "Invalid data",
                "details": {"animal_id": "Animal ID not found"},
            },
            400,
        ),
        (
            {
                "animal_id": "A-135792",
                "food_type": "Chicken Meat",
                "date": "18-06-2024",
                "time": "11.00",
            },
            {"error": "Missing fields ['employee_id']"},
            400,
        ),
    ],
)
def test_add_feeding_services(
    mock_feedings,
    mock_employees,
    mock_animals,
    input_data,
    expected_response,
    expected_status_code,
):
    result = add_feeding_services(input_data)
    assert result["response"] == expected_response
    assert result["status_code"] == expected_status_code


@pytest.mark.parametrize(
    "feeding_id, input_data, expected_response, expected_status_code",
    [
        (
            "F-123FEE",
            {
                "food_type": "Chicken Meat",
                "date": "18-06-2024",
                "time": "11.00",
            },
            {"success": "Feeding schedule is updated"},
            201,
        ),
        (
            "F-123FEE",
            {
                "food_type": "C",
                "date": "18-06-2024",
                "time": "11.00",
            },
            {
                "error": "Invalid data",
                "details": {
                    "food_type": "Food type must be between 2 and 64 characters"
                },
            },
            400,
        ),
        (
            "F-123FEE",
            {
                "food_tipe": "C",
                "date": "18-06-2024",
                "time": "11.00",
            },
            {"error": "Invalid input: Non-allowed fields ['food_tipe']"},
            400,
        ),
    ],
)
def test_update_feeding_services(
    mock_feedings,
    mock_employees,
    mock_animals,
    feeding_id,
    input_data,
    expected_response,
    expected_status_code,
):
    result = update_feeding_services(feeding_id, input_data)
    assert result["response"] == expected_response
    assert result["status_code"] == expected_status_code


def test_delete_feeding_services(mock_feedings, mock_employees):
    result = delete_feeding_services("F-123FEE")
    assert result["response"] == {"success": "Feeding schedule F-123FEE is deleted"}
    assert result["status_code"] == 200
