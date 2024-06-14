from repository.repository import animals, feedings, employees
from nanoid import generate
from datetime import datetime
import re


def data_validation(data):
    errors = {}

    if "animal_id" in data:
        animal_id = data["animal_id"]
        if animal_id not in animals:
            errors["animal_id"] = "Animal ID not found"

    if "employee_id" in data:
        employee_id = data["employee_id"]
        if employee_id not in employees:
            errors["employee_id"] = "Employee ID not found"

    if "food_type" in data:
        food_type = data["food_type"]
        if not 2 <= len(food_type) <= 64:
            errors["food_type"] = "Food type must be between 2 and 64 characters"

    if "date" in data:
        date = data["date"]
        try:
            datetime.strptime(date, "%d-%m-%Y")
        except ValueError:
            errors["date"] = "Date must be in the format 'dd-mm-yyyy'"

    if "time" in data:
        time = data["time"]
        if not re.match(r"^[0-2][0-9]\.[0-5][0-9]$", time):
            errors["time"] = "Time must be in the format 'HH.MM'"

    return errors


def add_feeding_services(data):
    validation_errors = data_validation(data)
    if validation_errors:
        return {
            "response": {"error": "Invalid data", "details": validation_errors},
            "status_code": 400,
        }

    required_fields = ["animal_id", "employee_id", "food_type", "date", "time"]

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {
            "response": {"error": f"Missing fields {missing_fields}"},
            "status_code": 400,
        }

    new_id = f"F-{generate('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ', 6)}"

    new_feeding = {
        "animal_id": data["animal_id"],
        "employee_id": data["employee_id"],
        "food_type": data["food_type"],
        "date": data["date"],
        "time": data["time"],
    }

    employees[data["employee_id"]]["schedule"].append(new_id)

    feedings[new_id] = new_feeding
    return {
        "response": {"success": "New schedule is added to feeding schedule database"},
        "status_code": 201,
    }


def update_feeding_services(feeding_id, data):
    validation_errors = data_validation(data)
    if validation_errors:
        return {
            "response": {"error": "Invalid data", "details": validation_errors},
            "status_code": 400,
        }

    allowed_fields = ["animal_id", "employee_id", "food_type", "date", "time"]

    if not all(key in allowed_fields for key in data):
        invalid_fields = [key for key in data if key not in allowed_fields]
        return {
            "response": {
                "error": f"Invalid input: Non-allowed fields {invalid_fields}"
            },
            "status_code": 400,
        }

    current_feedings = feedings[feeding_id]
    current_feedings.update(data)

    return {
        "response": {"success": "Feeding schedule is updated"},
        "status_code": 201,
    }


def delete_feeding_services(feeding_id):
    feeding = feedings.pop(feeding_id)
    employee_id = feeding["employee_id"]

    if employee_id in employees:
        try:
            employees[employee_id]["schedule"].remove(feeding_id)
        except ValueError:
            pass

    return {
        "response": {"success": f"Feeding schedule {feeding_id} is deleted"},
        "status_code": 200,
    }
