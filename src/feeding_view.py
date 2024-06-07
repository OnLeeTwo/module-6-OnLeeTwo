from flask import Blueprint, request, jsonify
from repository import animals, feedings

feeding_blueprint = Blueprint("feeding", __name__)


@feeding_blueprint.route("/feedings", methods=["GET"])
def get_feedings():
    """
    Get feeding schedule list
    ---
    responses:
        200:
            description: Return a list of feedings schedule
    """
    return jsonify(feedings), 200


@feeding_blueprint.route("/feedings/<int:feeding_id>", methods=["GET"])
def get_feeding_by_id(feeding_id):
    """
    Get feeding schedule list by Id
    ---
    responses:
        200:
            description: Return an feeding schedule with provided ID
        404:
            description: Return animal id not found
    """
    selected_feeding = feedings.get(feeding_id)
    if selected_feeding:
        return jsonify(selected_feeding)
    else:
        return jsonify({"error": "feeding id not found"}), 404


@feeding_blueprint.route("/feedings", methods=["POST"])
def add_feeding():
    """
    Create a new feeding schedule
    ---
    parameters:
      - name: feeding
        in: body
        schema:
            id: Feeding
            required:
                - animal_id
                - enclosure_id
                - food_type
                - date
                - time
            properties:
                animal_id:
                    type: string
                    description: The animal id of the feeding schedule to be added
                enclosure_id:
                    type: string
                    description: The enclosure id of the feeding schedule to be added
                food_type:
                    type: string
                    description: The food type of the feeding scheduleto be added
                date:
                    type: number
                    description: The date of the feeding schedule to be added
                time:
                    type: string
                    description: The time of the feeding schedule to be added
    responses:
        201:
            description: Feeding schedule created
        400:
            descrpition : No data provided or missing fields
    """
    if not request.json:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["animal_id", "enclosure_id", "food_type", "date", "time"]

    missing_fields = [field for field in required_fields if field not in request.json]
    if missing_fields:
        return jsonify({"error": f" Missing fields {missing_fields}"}), 400

    if not animals.get(request.json["animal_id"]):
        return (
            jsonify(
                {
                    "error": "Animal with ID that provided is not found on the animal list"
                }
            ),
            404,
        )

    new_id = max(feedings.keys()) + 1 if feedings else 1

    new_feeding = {
        "animal_id": request.json["animal_id"],
        "enclosure_id": request.json["enclosure_id"],
        "food_type": request.json["food_type"],
        "date": request.json["date"],
        "time": request.json["time"],
    }

    feedings[new_id] = new_feeding
    return jsonify({"success": f"New feeding schedule with ID {new_id} is added"}), 201


@feeding_blueprint.route("/feedings/<int:feeding_id>", methods=["PUT"])
def update_animal(feeding_id):
    """
    Update animal in database
    ---
    parameters:
      - name: feeding
        in: body
        schema:
            id: Feeding
            properties:
                animal_id:
                    type: string
                    description: The animal id of the feeding schedule to be added
                enclosure_id:
                    type: string
                    description: The enclosure id of the feeding schedule to be added
                food_type:
                    type: string
                    description: The food type of the feeding scheduleto be added
                date:
                    type: number
                    description: The date of the feeding schedule to be added
                time:
                    type: string
                    description: The time of the feeding schedule to be added
    responses:
        201:
            description: Feeding schedule updated
        400:
            descrpition : No data provided
        404:
            description : No animal ID on the animal list is found
    """
    if feeding_id not in feedings:
        return jsonify({"error": "Feeding schedule not found"}), 404

    if not request.json:
        return jsonify({"error": "No data provided"}), 400

    current_feeding = feedings[feeding_id]

    allowed_fields = ["animal_id", "enclosure_id", "food_type", "date", "time"]

    if not all(key in allowed_fields for key in request.json):
        invalid_fields = [key for key in request.json if key not in allowed_fields]
        return (
            jsonify({"error": f"Invalid input: Non-allowed fields {invalid_fields}"}),
            400,
        )

    if "animal_id" in request.json and not animals.get(request.json["animal_id"]):
        return (
            jsonify(
                {
                    "error": "Animal with ID that provided is not found on the animal list"
                }
            ),
            404,
        )

    updates = {
        key: request.json.get(key, current_feeding.get(key)) for key in allowed_fields
    }

    current_feeding.update(updates)

    return (
        jsonify({"success": f"Feeding schedule with ID {feeding_id} is updated"}),
        201,
    )


@feeding_blueprint.route("/feeding/<int:feeding_id>", methods=["DELETE"])
def delete_feeding(feeding_id):
    """
    Delete an feeding schedule by ID.
    ---
    parameters:
      - name: feeding_id
        in: path
        type: integer
        required: true
        description: ID of the feeding schedule to delete
    responses:
      200:
        description: Feeding schedule deleted successfully
      404:
        description: Feeding schedule not found
    """
    if feeding_id not in feedings:
        return jsonify({"error": "Feeding schedule not found"}), 404

    del feedings[feeding_id]

    return jsonify({"success": f"Feeding with ID {feeding_id} deleted"}), 200
