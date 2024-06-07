from flask import Blueprint, request, jsonify
from repository import animals_reports, visitors_reports, revenue_reports

report_blueprint = Blueprint("report", __name__)


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
