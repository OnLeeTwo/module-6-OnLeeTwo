import pytest
from app import app
from unittest.mock import patch

mock_visitors_reports = [
    {
        "ticket_type": "Adult",
        "date": "2024-06-01",
        "feedback_overall": "Positive",
        "number_of_visitors": 104,
    },
    {
        "ticket_type": "Child",
        "date": "2024-06-01",
        "feedback_overall": "Positive",
        "number_of_visitors": 52,
    },
    {
        "ticket_type": "Adult",
        "date": "2024-06-02",
        "feedback_overall": "Positive",
        "number_of_visitors": 125,
    },
    {
        "ticket_type": "Child",
        "date": "2024-06-02",
        "feedback_overall": "Positive",
        "number_of_visitors": 54,
    },
]

mock_revenue_reports = [
    {
        "ticket_type": "Adult",
        "event_type": "General Admission",
        "date": "2024-06-01",
        "revenue": 2000,
    },
    {
        "ticket_type": "Child",
        "event_type": "Special Exhibit",
        "date": "2024-06-01",
        "revenue": 500,
    },
    {
        "ticket_type": "Adult",
        "event_type": "General Admission",
        "date": "2024-06-02",
        "revenue": 2400,
    },
]

mock_animals_reports = [
    {
        "species": "Panthera leo",
        "gender_distribution": {"Male": 2, "Female": 1},
        "enclosure_distribution": {"Savannah": 2, "Jungle": 1},
    },
    {
        "species": "Loxodonta africana",
        "gender_distribution": {"Male": 0, "Female": 1},
        "enclosure_distribution": {"Savannah": 1},
    },
    {
        "species": "Aptenodytes forsteri",
        "gender_distribution": {"Male": 1, "Female": 0},
        "enclosure_distribution": {"Arctic": 1},
    },
]


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@patch("routes.report.animals", mock_animals_reports)
def test_get_animal_report(client):
    response = client.get("reports/animals")
    assert response.status_code == 200
    assert response.json == mock_animals_reports


@patch("routes.report.visitors_reports", mock_visitors_reports)
def test_get_visitor_report(client):
    response = client.get("reports/visitors")
    assert response.status_code == 200
    assert response.json == mock_visitors_reports


@patch("routes.report.revenue_reports", mock_revenue_reports)
def test_get_animal_report(client):
    response = client.get("reports/revenue")
    assert response.status_code == 200
    assert response.json == mock_revenue_reports
