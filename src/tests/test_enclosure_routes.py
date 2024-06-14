import pytest
from app import app
from flask import json
from unittest.mock import patch

mock_enclosures = {
    "EN-ENC123": {"name": "Savannah", "type": "Outdoor", "animals": []},
    "EN-123ENC": {"name": "Arctic", "type": "Outdoor", "animals": []},
}


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@patch("routes.enclosure.enclosures", mock_enclosures)
def test_get_enclosure(client):
    response = client.get("/enclosure")
    assert response.status_code == 200
    assert response.json == mock_enclosures


@patch("routes.enclosure.enclosures", mock_enclosures)
def test_get_enclosure_by_id(client):
    response = client.get("/enclosure/EN-ENC123")
    assert response.status_code == 200
    assert response.json == mock_enclosures["EN-ENC123"]

    response = client.get("/enclosure/INVALID_ID")
    assert response.status_code == 404
    assert response.json == {"error": "enclosure id not found"}


@patch("routes.enclosure.enclosures", mock_enclosures)
@patch("routes.enclosure.add_enclosure_services")
def test_add_enclosure(mock_add_enclosure_services, client):
    mock_add_enclosure_services.return_value = {
        "response": {"success": "Jungle is added to enclosure database"},
        "status_code": 201,
    }

    new_enclosure = {
        "name": "Jungle",
        "type": "Outdoor",
    }

    response = client.post(
        "/enclosure", data=json.dumps(new_enclosure), content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json == {"success": "Jungle is added to enclosure database"}

    response = client.post(
        "/enclosure", data=json.dumps({}), content_type="application/json"
    )
    assert response.status_code == 400
    assert response.json == {"error": "No data provided"}


@patch("routes.enclosure.enclosures", mock_enclosures)
@patch("routes.enclosure.update_enclosure_services")
def test_update_enclosure(mock_update_enclosure_services, client):
    mock_update_enclosure_services.return_value = {
        "response": {"success": "Forest is updated"},
        "status_code": 201,
    }

    response = client.put(
        "/enclosure/EN-ENC123",
        data=json.dumps({"name": "Forest"}),
        content_type="application/json",
    )
    assert response.status_code == 201
    assert response.json == {"success": "Forest is updated"}

    response = client.put(
        "/enclosure/INVALID_ID",
        data=json.dumps({"name": "Forest"}),
        content_type="application/json",
    )
    assert response.status_code == 404
    assert response.json == {"error": "enclosure id not found"}

    response = client.put(
        "/enclosure/EN-ENC123", data=json.dumps({}), content_type="application/json"
    )
    assert response.status_code == 400
    assert response.json == {"error": "No data provided"}


@patch("routes.enclosure.enclosures", mock_enclosures)
@patch("routes.enclosure.delete_enclosure_services")
def test_delete_enclosure(mock_delete_enclosure_services, client):
    mock_delete_enclosure_services.return_value = {
        "response": {"success": "Enclosure with ID EN-ENC123 deleted"},
        "status_code": 201,
    }

    response = client.delete("/enclosure/EN-ENC123")

    assert response.status_code == 201
    assert response.json == {"success": "Enclosure with ID EN-ENC123 deleted"}

    response = client.delete("/enclosure/INVALID_ID")

    assert response.status_code == 404
    assert response.json == {"error": "Enclosure ID not found"}
