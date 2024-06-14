from flask import Blueprint, jsonify
from flasgger import swag_from
from services.report import generate_animal_reports
from repository.repository import (
    visitors_reports,
    revenue_reports,
    animals,
    enclosures,
)

report_blueprint = Blueprint("report", __name__)


@report_blueprint.route("/reports/animals", methods=["GET"])
@swag_from("../docs/report/get_animal_reports.yml")
def get_animal_reports():
    # Generate the reports
    new_reports = generate_animal_reports(animals, enclosures)

    global animals_reports
    animals_reports = new_reports

    return jsonify(animals_reports), 200


@report_blueprint.route("/reports/visitors", methods=["GET"])
@swag_from("../docs/report/get_visitor_reports.yml")
def get_visitor_reports():
    return jsonify(visitors_reports), 200


@report_blueprint.route("/reports/revenue", methods=["GET"])
@swag_from("../docs/report/get_revenue_reports.yml")
def get_revenue_reports():
    return jsonify(revenue_reports), 200
