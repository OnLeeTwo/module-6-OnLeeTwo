from flask import Blueprint, request, jsonify
from flasgger import swag_from
from repository.repository import animals
from services.animal import add_animal_services, update_animal_services

animal_blueprint = Blueprint("animal", __name__)


@animal_blueprint.route("/animal", methods=["GET"])
@swag_from("../docs/animal/get_animal.yml")
def get_animal():
    return jsonify(animals), 200


@animal_blueprint.route("/animal/<string:animal_id>", methods=["GET"])
@swag_from("../docs/animal/get_animal_by_id.yml")
def get_animal_by_id(animal_id):
    selected_animal = animals.get(animal_id)
    if selected_animal:
        return jsonify(selected_animal)
    return jsonify({"error": "Animal id not found"}), 404


@animal_blueprint.route("/animal", methods=["POST"])
@swag_from("../docs/animal/add_animal.yml")
def add_animal():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    result = add_animal_services(data)
    return jsonify(result["response"]), result["status_code"]


@animal_blueprint.route("/animal/<string:animal_id>", methods=["PUT"])
@swag_from("../docs/animal/update_animal.yml")
def update_animal(animal_id):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if animal_id not in animals:
        return jsonify({"error": "Animal not found"}), 404

    result = update_animal_services(animal_id, data)
    return jsonify(result["response"]), result["status_code"]


@animal_blueprint.route("/animal/<string:animal_id>", methods=["DELETE"])
@swag_from("../docs/animal/delete_animal.yml")
def delete_animal(animal_id):
    if animal_id not in animals:
        return jsonify({"error": "Animal not found"}), 404

    del animals[animal_id]

    return jsonify({"success": f"Animal with ID {animal_id} deleted"}), 200
