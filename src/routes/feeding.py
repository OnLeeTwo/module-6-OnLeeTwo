from flask import Blueprint, request, jsonify
from flasgger import swag_from
from repository.repository import feedings
from services.feeding import (
    add_feeding_services,
    update_feeding_services,
    delete_feeding_services,
)

feeding_blueprint = Blueprint("feeding", __name__)


@feeding_blueprint.route("/feeding", methods=["GET"])
@swag_from("../docs/feeding/get_feeding.yml")
def get_feeding():
    return jsonify(feedings), 200


@feeding_blueprint.route("/feeding/<string:feeding_id>", methods=["GET"])
@swag_from("../docs/feeding/get_feeding_by_id.yml")
def get_feeding_by_id(feeding_id):
    selected_feeding = feedings.get(feeding_id)
    if selected_feeding:
        return jsonify(selected_feeding)
    return jsonify({"error": "feeding id not found"}), 404


@feeding_blueprint.route("/feeding", methods=["POST"])
@swag_from("../docs/feeding/add_feeding.yml")
def add_feeding():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    result = add_feeding_services(data)
    return jsonify(result["response"]), result["status_code"]


@feeding_blueprint.route("/feeding/<string:feeding_id>", methods=["PUT"])
@swag_from("../docs/feeding/update_feeding.yml")
def update_feeding(feeding_id):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if feeding_id not in feedings:
        return jsonify({"error": "feeding not found"}), 404

    result = update_feeding_services(feeding_id, data)
    return jsonify(result["response"]), result["status_code"]


@feeding_blueprint.route("/feeding/<string:feeding_id>", methods=["DELETE"])
@swag_from("../docs/feeding/delete_feeding.yml")
def delete_feeding(feeding_id):
    if feeding_id not in feedings:
        return jsonify({"error": "feeding not found"}), 404

    result = delete_feeding_services(feeding_id)
    return jsonify(result["response"]), result["status_code"]
