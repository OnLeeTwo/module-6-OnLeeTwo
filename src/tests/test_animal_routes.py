import pytest
from app import app
from flask import json
from unittest.mock import patch

mock_animals = {
    "A-ASD545": {
        "name": "Leo",
        "species": "Lion",
        "familia": "Felidae",
        "age": 5,
        "gender": "Male",
    },
    "A-79WE4E": {
        "name": "Ellie",
        "species": "Elephant",
        "familia": "Elephantidae",
        "age": 10,
        "gender": "Female",
    },
}


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@patch("routes.animal.animals", mock_animals)
def test_get_animal(client):
    response = client.get("/animal")
    assert response.status_code == 200
    assert response.json == mock_animals


@patch("routes.animal.animals", mock_animals)
def test_get_animal_by_id(client):
    response = client.get("/animal/A-ASD545")
    assert response.status_code == 200
    assert response.json == mock_animals["A-ASD545"]

    response = client.get("/animal/INVALID_ID")
    assert response.status_code == 404
    assert response.json == {"error": "Animal id not found"}


@patch("routes.animal.animals", mock_animals)
@patch("routes.animal.add_animal_services")
def test_add_animal(mock_add_animal_services, client):
    mock_add_animal_services.return_value = {
        "response": {"success": "Tiger is added to animal database"},
        "status_code": 201,
    }

    new_animal = {
        "name": "Tiger",
        "species": "Tiger",
        "familia": "Felidae",
        "age": 3,
        "gender": "Female",
    }

    response = client.post(
        "/animal", data=json.dumps(new_animal), content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json == {"success": "Tiger is added to animal database"}

    response = client.post(
        "/animal", data=json.dumps({}), content_type="application/json"
    )
    assert response.status_code == 400
    assert response.json == {"error": "No data provided"}


@patch("routes.animal.animals", mock_animals)
@patch("routes.animal.update_animal_services")
def test_update_animal(mock_update_animal_services, client):
    mock_update_animal_services.return_value = {
        "response": {"success": "Loe is updated"},
        "status_code": 201,
    }

    response = client.put(
        "/animal/A-ASD545",
        data=json.dumps({"name": "Loe"}),
        content_type="application/json",
    )
    assert response.status_code == 201
    assert response.json == {"success": "Loe is updated"}

    response = client.put(
        "/animal/INVALID_ID",
        data=json.dumps({"name": "Loe"}),
        content_type="application/json",
    )
    assert response.status_code == 404
    assert response.json == {"error": "Animal not found"}

    response = client.put(
        "/animal/A-ASD545", data=json.dumps({}), content_type="application/json"
    )
    assert response.status_code == 400
    assert response.json == {"error": "No data provided"}


@patch("routes.animal.animals", mock_animals)
def test_delete_animal(client):
    original_mock_animals = dict(mock_animals)

    response = client.delete("/animal/A-ASD545")

    assert response.status_code == 200
    assert response.json == {"success": "Animal with ID A-ASD545 deleted"}

    assert "A-ASD545" not in mock_animals
    assert len(mock_animals) == len(original_mock_animals) - 1

    assert "A-79WE4E" in mock_animals
    assert mock_animals["A-79WE4E"] == original_mock_animals["A-79WE4E"]

    response = client.delete("/animal/INVALID_ID")

    assert response.status_code == 404
    assert response.json == {"error": "Animal not found"}
