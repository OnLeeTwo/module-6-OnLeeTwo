from flask import Blueprint, request, jsonify
from animal_view import animals

report_blueprint = Blueprint("report", __name__)

visitors_reports = [
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

revenue_reports = [
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

animals_reports = [
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


@report_blueprint.route("/reports/animals", methods=["GET"])
def get_animals_reports():
    """
    Get animal reports
    ---
    responses:
        200:
            description: Return a list of animal reports
    """
    return jsonify(animals_reports), 200


@report_blueprint.route("/reports/visitors", methods=["GET"])
def get_visitors_reports():
    """
    Get visitors reports
    ---
    responses:
        200:
            description: Return a list of visitor reports
    """
    return jsonify(visitors_reports), 200


@report_blueprint.route("/reports/revenue", methods=["GET"])
def get_revenue_reports():
    """
    Get reveune reports
    ---
    responses:
        200:
            description: Return a list of revenue reports
    """
    return jsonify(revenue_reports), 200
