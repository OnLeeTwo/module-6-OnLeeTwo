from repository.repository import enclosures
from nanoid import generate


def data_validation(data):
    errors = {}

    if "name" in data:
        name = data["name"]
        if not 2 <= len(name) <= 64:
            errors["name"] = "Name must be between 2 and 64 characters"

    if "type" in data:
        type = data["type"]
        if not 2 <= len(type) <= 64:
            errors["type"] = "Type must be between 2 and 64 characters"

    return errors


def add_enclosure_services(data):
    validation_errors = data_validation(data)
    if validation_errors:
        return {
            "response": {"error": "Invalid data", "details": validation_errors},
            "status_code": 400,
        }

    required_fields = ["name", "type"]

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {
            "response": {"error": f"Missing fields {missing_fields}"},
            "status_code": 400,
        }

    new_id = f"EN-{generate('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ', 6)}"

    new_enclosure = {
        "name": data["name"],
        "type": data["type"],
        "animal": [],
    }

    enclosures[new_id] = new_enclosure
    return {
        "response": {
            "success": f"{new_enclosure['name']} is added to enclosure database"
        },
        "status_code": 201,
    }


def update_enclosure_services(enclosure_id, data):
    validation_errors = data_validation(data)
    if validation_errors:
        return {
            "response": {"error": "Invalid data", "details": validation_errors},
            "status_code": 400,
        }

    allowed_fields = ["name", "type"]

    if not all(key in allowed_fields for key in data):
        invalid_fields = [key for key in data if key not in allowed_fields]
        return {
            "response": {
                "error": f"Invalid input: Non-allowed fields {invalid_fields}"
            },
            "status_code": 400,
        }

    current_enclosure = enclosures[enclosure_id]
    current_enclosure.update(data)

    return {
        "response": {"success": f"{current_enclosure['name']} is updated"},
        "status_code": 201,
    }


def delete_enclosure_services(enclosure_id):
    current_enclosure = enclosures[enclosure_id]

    if current_enclosure["animals"]:
        return {
            "response": {
                "error": "Enclosure is not empty, relocate the animal inhabiting first!"
            },
            "status_code": 400,
        }

    del enclosures[enclosure_id]

    return {
        "response": {"success": f"Enclosure with ID {enclosure_id} is deleted"},
        "status_code": 200,
    }
