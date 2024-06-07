from flask import Blueprint, request, jsonify
from repository import animals

animal_blueprint = Blueprint("animal", __name__)


@animal_blueprint.route("/animal", methods=["GET"])
def get_animals():
    """
    Get animal list
    ---
    responses:
        200:
            description: Return a list of animal
    """
    return jsonify(animals), 200


@animal_blueprint.route("/animal/<int:animal_id>", methods=["GET"])
def get_animal_by_id(animal_id):
    """
    Get animal list by Id
    ---
    responses:
        200:
            description: Return an animal with provided ID
        404:
            description: Return animal id not found
    """
    selected_animal = animals.get(animal_id)
    if selected_animal:
        return jsonify(selected_animal)
    else:
        return jsonify({"error": "Animal id not found"}), 404


@animal_blueprint.route("/animal", methods=["POST"])
def add_animal():
    """
    Create a new animal
    ---
    parameters:
      - name: animal
        in: body
        schema:
            id: Animal
            required:
                - name
                - species
                - familia
                - age
                - gender
            properties:
                name:
                    type: string
                    description: The name of the animal to be added
                species:
                    type: string
                    description: The species of the animal to be added
                familia:
                    type: string
                    description: The familia of the animal to be added
                age:
                    type: number
                    description: The age of the animal to be added
                gender:
                    type: string
                    description: The gender of the animal to be added
    responses:
        201:
            description: Animal created
        400:
            descrpition : No data provided or missing fields
    """
    if not request.json:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["name", "species", "familia", "age", "gender"]

    missing_fields = [field for field in required_fields if field not in request.json]
    if missing_fields:
        return jsonify({"error": f" Missing fields {missing_fields}"}), 400

    new_id = max(animals.keys()) + 1 if animals else 1

    new_animal = {
        "name": request.json["name"],
        "species": request.json["species"],
        "familia": request.json["familia"],
        "age": request.json["age"],
        "gender": request.json["gender"],
    }

    animals[new_id] = new_animal
    return jsonify({"success": f"{new_animal['name']} is added"}), 201


@animal_blueprint.route("/animal/<int:animal_id>", methods=["PUT"])
def update_animal(animal_id):
    """
    Update animal in database
    ---
    parameters:
      - name: animal
        in: body
        schema:
            id: Animal
            properties:
                name:
                    type: string
                    description: The name of the animal to be added
                species:
                    type: string
                    description: The species of the animal to be added
                familia:
                    type: string
                    description: The familia of the animal to be added
                age:
                    type: number
                    description: The age of the animal to be added
                gender:
                    type: string
                    description: The gender of the animal to be added
    responses:
        201:
            description: Animal updated
        400:
            descrpition : No data provided
    """
    if animal_id not in animals:
        return jsonify({"error": "Animal not found"}), 404

    if not request.json:
        return jsonify({"error": "No data provided"}), 400

    current_animal = animals[animal_id]

    allowed_fields = ["name", "species", "familia", "age", "gender"]

    if not all(key in allowed_fields for key in request.json):
        invalid_fields = [key for key in request.json if key not in allowed_fields]
        return (
            jsonify({"error": f"Invalid input: Non-allowed fields {invalid_fields}"}),
            400,
        )

    updates = {
        key: request.json.get(key, current_animal.get(key)) for key in allowed_fields
    }

    current_animal.update(updates)

    return jsonify({"success": f"{current_animal['name']} is updated"}), 201


@animal_blueprint.route("/animal/<int:animal_id>", methods=["DELETE"])
def delete_animal(animal_id):
    """
    Delete an animal by ID.
    ---
    parameters:
      - name: animal_id
        in: path
        type: integer
        required: true
        description: ID of the animal to delete
    responses:
      200:
        description: Animal deleted successfully
      404:
        description: Animal not found
    """
    if animal_id not in animals:
        return jsonify({"error": "Animal not found"}), 404

    del animals[animal_id]

    return jsonify({"success": f"Animal with ID {animal_id} deleted"}), 200
