import pytest
from app import app
from flask import json
from unittest.mock import patch

mock_feedings = {
    "F-123FEE": {
        "animal_id": "A-123456",
        "feeding_id": "E-789ABC",
        "food_type": "Pellets",
        "date": "12-06-2024",
        "time": "10.30",
    },
    "F-FEE123": {
        "animal_id": "A-987654",
        "feeding_id": "E-XYZ123",
        "food_type": "Vegetables",
        "date": "15-06-2024",
        "time": "12.45",
    },
}


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@patch("routes.feeding.feedings", mock_feedings)
def test_get_feeding(client):
    response = client.get("/feeding")
    assert response.status_code == 200
    assert response.json == mock_feedings


@patch("routes.feeding.feedings", mock_feedings)
def test_get_feeding_by_id(client):
    response = client.get("/feeding/F-123FEE")
    assert response.status_code == 200
    assert response.json == mock_feedings["F-123FEE"]

    response = client.get("/feeding/INVALID_ID")
    assert response.status_code == 404
    assert response.json == {"error": "feeding id not found"}


@patch("routes.feeding.feedings", mock_feedings)
@patch("routes.feeding.add_feeding_services")
def test_add_feeding(mock_add_feeding_services, client):
    mock_add_feeding_services.return_value = {
        "response": {"success": "New schedule is added to feeding schedule database"},
        "status_code": 201,
    }

    new_feeding = {
        "animal_id": "A-456789",
        "employee_id": "E-DEF456",
        "food_type": "Fish",
        "date": "16-06-2024",
        "time": "09.15",
    }

    response = client.post(
        "/feeding", data=json.dumps(new_feeding), content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json == {
        "success": "New schedule is added to feeding schedule database"
    }

    response = client.post(
        "/feeding", data=json.dumps({}), content_type="application/json"
    )
    assert response.status_code == 400
    assert response.json == {"error": "No data provided"}


@patch("routes.feeding.feedings", mock_feedings)
@patch("routes.feeding.update_feeding_services")
def test_update_feeding(mock_update_feeding_services, client):
    mock_update_feeding_services.return_value = {
        "response": {"success": "Feeding schedule is updated"},
        "status_code": 201,
    }

    response = client.put(
        "/feeding/F-123FEE",
        data=json.dumps({"food_type": "Shrimps"}),
        content_type="application/json",
    )
    assert response.status_code == 201
    assert response.json == {"success": "Feeding schedule is updated"}

    response = client.put(
        "/feeding/INVALID_ID",
        data=json.dumps({"food_type": "Shrimps"}),
        content_type="application/json",
    )
    assert response.status_code == 404
    assert response.json == {"error": "feeding not found"}

    response = client.put(
        "/feeding/F-123FEE", data=json.dumps({}), content_type="application/json"
    )
    assert response.status_code == 400
    assert response.json == {"error": "No data provided"}


@patch("routes.feeding.feedings", mock_feedings)
@patch("routes.feeding.delete_feeding_services")
def test_delete_feeding(mock_delete_feeding_services, client):
    mock_delete_feeding_services.return_value = {
        "response": {"success": "Feeding schedule F-123FEE is deleted"},
        "status_code": 201,
    }

    response = client.delete("/feeding/F-123FEE")

    assert response.status_code == 201
    assert response.json == {"success": "Feeding schedule F-123FEE is deleted"}

    response = client.delete("/feeding/INVALID_ID")

    assert response.status_code == 404
    assert response.json == {"error": "feeding not found"}
