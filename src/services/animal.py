from repository.repository import animals, enclosures
from nanoid import generate


def data_validation(data):
    errors = {}

    if "name" in data:
        name = data["name"]
        if not 2 <= len(name) <= 64:
            errors["name"] = "Name must be between 2 and 64 characters"

    if "species" in data:
        species = data["species"]
        if not 2 <= len(species) <= 64:
            errors["species"] = "Species must be between 2 and 64 characters"

    if "familia" in data:
        familia = data["familia"]
        if not 2 <= len(familia) <= 64:
            errors["familia"] = "Familia must be between 2 and 64 characters"

    if "age" in data:
        age = data["age"]
        if not isinstance(age, int) or age < 0:
            errors["age"] = "Age must be a non-negative number"

    if "gender" in data:
        gender = data["gender"].lower()
        if gender not in ["female", "male"]:
            errors["gender"] = "Gender must be 'female' or 'male'"

    return errors


def add_animal_services(data):
    validation_errors = data_validation(data)
    if validation_errors:
        return {
            "response": {"error": "Invalid data", "details": validation_errors},
            "status_code": 400,
        }

    required_fields = ["name", "species", "familia", "age", "gender", "enclosure_id"]

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {
            "response": {"error": f"Missing fields {missing_fields}"},
            "status_code": 400,
        }

    enclosure_id = data["enclosure_id"]
    if enclosure_id not in enclosures:
        return {
            "response": {"error": "Enclosure ID is not found"},
            "status_code": 404,
        }

    new_id = f"A-{generate('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ', 6)}"

    new_animal = {
        "enclosure_id": enclosure_id,
        "name": data["name"],
        "species": data["species"],
        "familia": data["familia"],
        "age": data["age"],
        "gender": data["gender"],
    }

    enclosures[enclosure_id]["animals"].append(new_id)

    animals[new_id] = new_animal
    return {
        "response": {"success": f"{new_animal['name']} is added to animal database"},
        "status_code": 201,
    }


def update_animal_services(animal_id, data):
    validation_errors = data_validation(data)
    if validation_errors:
        return {
            "response": {"error": "Invalid data", "details": validation_errors},
            "status_code": 400,
        }

    allowed_fields = ["name", "species", "familia", "age", "gender"]

    if not all(key in allowed_fields for key in data):
        invalid_fields = [key for key in data if key not in allowed_fields]
        return {
            "response": {
                "error": f"Invalid input: Non-allowed fields {invalid_fields}"
            },
            "status_code": 400,
        }

    current_animal = animals[animal_id]
    current_animal.update(data)

    return {
        "response": {"success": f"{current_animal['name']} is updated"},
        "status_code": 201,
    }
