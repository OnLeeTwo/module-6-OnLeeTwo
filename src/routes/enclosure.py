from flask import Blueprint, request, jsonify
from flasgger import swag_from
from repository.repository import enclosures
from services.enclosure import (
    add_enclosure_services,
    update_enclosure_services,
    delete_enclosure_services,
)

enclosure_blueprint = Blueprint("enclosure", __name__)


@enclosure_blueprint.route("/enclosure", methods=["GET"])
@swag_from("../docs/enclosure/get_enclosure.yml")
def get_enclosure():
    return jsonify(enclosures), 200


@enclosure_blueprint.route("/enclosure/<string:enclosure_id>", methods=["GET"])
@swag_from("../docs/enclosure/get_enclosure_by_id.yml")
def get_enclosure_by_id(enclosure_id):
    selected_enclosure = enclosures.get(enclosure_id)
    if selected_enclosure:
        return jsonify(selected_enclosure)
    return jsonify({"error": "enclosure id not found"}), 404


@enclosure_blueprint.route("/enclosure", methods=["POST"])
@swag_from("../docs/enclosure/add_enclosure.yml")
def add_enclosure():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    result = add_enclosure_services(data)
    return jsonify(result["response"]), result["status_code"]


@enclosure_blueprint.route("/enclosure/<string:enclosure_id>", methods=["PUT"])
@swag_from("../docs/enclosure/update_enclosure.yml")
def update_enclosure(enclosure_id):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if enclosure_id not in enclosures:
        return jsonify({"error": "enclosure id not found"}), 404

    result = update_enclosure_services(enclosure_id, data)
    return jsonify(result["response"]), result["status_code"]


@enclosure_blueprint.route("/enclosure/<string:enclosure_id>", methods=["DELETE"])
@swag_from("../docs/enclosure/delete_enclosure.yml")
def delete_enclosure(enclosure_id):
    if enclosure_id not in enclosures:
        return jsonify({"error": "Enclosure ID not found"}), 404

    result = delete_enclosure_services(enclosure_id)
    return jsonify(result["response"]), result["status_code"]
