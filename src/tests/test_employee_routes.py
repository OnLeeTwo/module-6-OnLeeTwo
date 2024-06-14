import pytest
from app import app
from flask import json
from unittest.mock import patch

mock_employees = {
    "E-123EMP": {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "+62234567890",
        "role": "Zoo Keeper",
        "schedule": [],
    },
    "E-EMP123": {
        "name": "Alice Smith",
        "email": "alice.smith@example.com",
        "phone": "+62987654321",
        "role": "Zoo Manager",
        "schedule": [],
    },
}


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@patch("routes.employee.employees", mock_employees)
def test_get_employee(client):
    response = client.get("/employees")
    assert response.status_code == 200
    assert response.json == mock_employees


@patch("routes.employee.employees", mock_employees)
def test_get_employee_by_id(client):
    response = client.get("/employees/E-EMP123")
    assert response.status_code == 200
    assert response.json == mock_employees["E-EMP123"]

    response = client.get("/employees/INVALID_ID")
    assert response.status_code == 404
    assert response.json == {"error": "employee id not found"}


@patch("routes.employee.employees", mock_employees)
@patch("routes.employee.add_employee_services")
def test_add_employee(mock_add_employee_services, client):
    mock_add_employee_services.return_value = {
        "response": {"success": "Michael Johnson is added to employee database"},
        "status_code": 201,
    }

    new_employee = {
        "name": "Michael Johnson",
        "email": "michael.johnson@example.com",
        "phone": "+62765432890",
        "role": "Zoo Security",
    }

    response = client.post(
        "/employees", data=json.dumps(new_employee), content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json == {"success": "Michael Johnson is added to employee database"}

    response = client.post(
        "/employees", data=json.dumps({}), content_type="application/json"
    )
    assert response.status_code == 400
    assert response.json == {"error": "No data provided"}


@patch("routes.employee.employees", mock_employees)
@patch("routes.employee.update_employee_services")
def test_update_employee(mock_update_employee_services, client):
    mock_update_employee_services.return_value = {
        "response": {"success": "Dohn Joe is updated"},
        "status_code": 201,
    }

    response = client.put(
        "/employees/E-123EMP",
        data=json.dumps({"name": "Dohn Joe"}),
        content_type="application/json",
    )
    assert response.status_code == 201
    assert response.json == {"success": "Dohn Joe is updated"}

    response = client.put(
        "/employees/INVALID_ID",
        data=json.dumps({"name": "Dohn Joe"}),
        content_type="application/json",
    )
    assert response.status_code == 404
    assert response.json == {"error": "Employee not found"}

    response = client.put(
        "/employees/E-123EMP", data=json.dumps({}), content_type="application/json"
    )
    assert response.status_code == 400
    assert response.json == {"error": "No data provided"}


@patch("routes.employee.employees", mock_employees)
@patch("routes.employee.delete_employee_services")
def test_delete_employee(mock_delete_employee_services, client):
    mock_delete_employee_services.return_value = {
        "response": {"success": "Employee E-123EMP and their schedules are deleted"},
        "status_code": 201,
    }

    response = client.delete("/employees/E-123EMP")

    assert response.status_code == 201
    assert response.json == {
        "success": "Employee E-123EMP and their schedules are deleted"
    }

    response = client.delete("/employees/INVALID_ID")

    assert response.status_code == 404
    assert response.json == {"error": "Employee not found"}
