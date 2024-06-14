import pytest
from unittest.mock import patch
from services.employee import (
    data_validation,
    add_employee_services,
    update_employee_services,
    delete_employee_services,
)


@pytest.fixture
def mock_employees():
    with patch(
        "services.employee.employees",
        {
            "E-123456": {
                "name": "John Doe",
                "email": "johndoe@example.com",
                "phone": "+62234567890",
                "role": "Zoo Keeper",
                "schedule": [],
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
                "name": "John Doe",
                "email": "johndoe@example.com",
                "phone": "+62234567890",
                "role": "Zoo Keeper",
            },
            {},
        ),
        (
            {
                "name": "J",
                "email": "johndoe@example.com",
                "phone": "+62234567890",
                "role": "Zoo Keeper",
            },
            {"name": "Name must be between 2 and 64 characters"},
        ),
        (
            {
                "name": "John Doe",
                "email": "johndoe@example.com",
                "phone": "+32",
                "role": "Zoo Keeper",
            },
            {
                "phone": "Invalid phone format",
            },
        ),
        (
            {
                "name": "John Doe",
                "email": "johndoe@example.com",
                "phone": "+32",
                "role": "Z",
            },
            {
                "role": "Role must be between 2 and 64 characters",
                "phone": "Invalid phone format",
            },
        ),
        (
            {
                "name": "John Doe",
                "email": "johndoe.example.com",
                "phone": "+62234567890",
                "role": "Zoo Keeper",
            },
            {"email": "Invalid email format"},
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
                "name": "Michael Johnson",
                "email": "michael.johnson@example.com",
                "phone": "+62765432890",
                "role": "Zoo Security",
            },
            {"success": "Michael Johnson is added to employee database"},
            201,
        ),
        (
            {
                "name": "Michael Johnson",
                "email": "michael.johnson@example.com",
                "phone": "+62765432890",
            },
            {"error": "Missing fields ['role']"},
            400,
        ),
        (
            {
                "name": "Michael Johnson",
                "email": "abcdefg.com",
                "phone": "+62765432890",
                "role": "Zoo Security",
            },
            {"error": "Invalid data", "details": {"email": "Invalid email format"}},
            400,
        ),
    ],
)
def test_add_employee_services(
    mock_employees, input_data, expected_response, expected_status_code
):
    result = add_employee_services(input_data)
    assert result["response"] == expected_response
    assert result["status_code"] == expected_status_code


@pytest.mark.parametrize(
    "employee_id, input_data, expected_response, expected_status_code",
    [
        (
            "E-123456",
            {
                "name": "Michael Johnson",
                "email": "michael.johnson@example.com",
                "phone": "+62765432890",
                "role": "Zoo Security",
            },
            {"success": "Michael Johnson is updated"},
            201,
        ),
        (
            "E-123456",
            {
                "name": "Michael Johnson",
                "phone": "+62765432890",
                "e-mail": "adsas.com",
                "role": "Zoo Security",
            },
            {"error": "Invalid input: Non-allowed fields ['e-mail']"},
            400,
        ),
        (
            "E-123456",
            {
                "name": "Michael Johnson",
                "email": "invalid_email_format",
                "phone": "+62765432890",
                "role": "Zoo Security",
            },
            {"error": "Invalid data", "details": {"email": "Invalid email format"}},
            400,
        ),
    ],
)
def test_update_employee_services(
    mock_employees, employee_id, input_data, expected_response, expected_status_code
):
    result = update_employee_services(employee_id, input_data)
    assert result["response"] == expected_response
    assert result["status_code"] == expected_status_code


@pytest.mark.parametrize(
    "employee_id, expected_response, expected_status_code",
    [
        (
            "E-123456",
            {"success": "Employee E-123456 and their schedules are deleted"},
            200,
        ),
    ],
)
def test_delete_employee_services(
    mock_employees, employee_id, expected_response, expected_status_code
):
    result = delete_employee_services(employee_id)
    assert result["response"] == expected_response
    assert result["status_code"] == expected_status_code
