from repository.repository import employees, feedings
import re
from nanoid import generate


def data_validation(data):
    errors = {}

    if "name" in data:
        name = data["name"]
        if not 2 <= len(name) <= 64:
            errors["name"] = "Name must be between 2 and 64 characters"

    if "email" in data:
        email = data["email"]
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors["email"] = "Invalid email format"

    if "phone" in data:
        phone = data["phone"]
        if not re.match(r"^\+?\d{1,3}?\d{9,15}$", phone):
            errors["phone"] = "Invalid phone format"

    if "role" in data:
        role = data["role"]
        if not 2 <= len(role) <= 64:
            errors["role"] = "Role must be between 2 and 64 characters"

    return errors


def add_employee_services(data):
    validation_errors = data_validation(data)
    if validation_errors:
        return {
            "response": {"error": "Invalid data", "details": validation_errors},
            "status_code": 400,
        }

    required_fields = ["name", "email", "phone", "role"]

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {
            "response": {"error": f"Missing fields {missing_fields}"},
            "status_code": 400,
        }

    new_id = f"E-{generate('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ', 6)}"

    new_employee = {
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"],
        "role": data["role"],
        "schedule": [],
    }

    employees[new_id] = new_employee
    return {
        "response": {
            "success": f"{new_employee['name']} is added to employee database"
        },
        "status_code": 201,
    }


def update_employee_services(employee_id, data):
    validation_errors = data_validation(data)
    if validation_errors:
        return {
            "response": {"error": "Invalid data", "details": validation_errors},
            "status_code": 400,
        }

    allowed_fields = ["name", "email", "phone", "role"]

    if not all(key in allowed_fields for key in data):
        invalid_fields = [key for key in data if key not in allowed_fields]
        return {
            "response": {
                "error": f"Invalid input: Non-allowed fields {invalid_fields}"
            },
            "status_code": 400,
        }

    current_employee = employees[employee_id]
    current_employee.update(data)

    return {
        "response": {"success": f"{current_employee['name']} is updated"},
        "status_code": 201,
    }


def delete_employee_services(employee_id):
    schedule = employees[employee_id].get("schedule", [])

    del employees[employee_id]

    for feeding_id in schedule:
        if feeding_id in feedings:
            del feedings[feeding_id]

    return {
        "response": {
            "success": f"Employee {employee_id} and their schedules are deleted"
        },
        "status_code": 200,
    }
