from flask import Blueprint, request, jsonify
from repository import employees

employee_blueprint = Blueprint("employees", __name__)


@employee_blueprint.route("/employees", methods=["GET"])
def get_employee():
    """
    Get employee list
    ---
    responses:
        200:
            description: Return a list of employee
    """
    return jsonify(employees), 200


@employee_blueprint.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee_by_id(employee_id):
    """
    Get employee list by ID
    ---
    responses:
        200:
            description: Return an employee with provided ID
        404:
            description: Return employee id not found
    """
    selected_employee = employees.get(employee_id)
    if selected_employee:
        return jsonify(selected_employee)
    else:
        return jsonify({"error": "employee id not found"}), 404


@employee_blueprint.route("/employees", methods=["POST"])
def add_employee():
    """
    Create a new employee
    ---
    parameters:
      - name: employee
        in: body
        schema:
            id: employee
            required:
                - name
                - email
                - phone
                - role
                - schedule
            properties:
                name:
                    type: string
                    description: The name of the employee to be added
                email:
                    type: string
                    description: The email of the employee to be added
                phone:
                    type: string
                    description: The phone of the employee to be added
                role:
                    type: number
                    description: The role of the employee to be added
                schedule:
                    type: string
                    description: The gender of the employee to be added
    responses:
        201:
            description: employee created
        400:
            descrpition : No data provided or missing fields
    """
    if not request.json:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["name", "email", "phone", "role", "schedule"]

    missing_fields = [field for field in required_fields if field not in request.json]
    if missing_fields:
        return jsonify({"error": f" Missing fields {missing_fields}"}), 400

    new_id = max(employees.keys()) + 1 if employees else 1

    new_employee = {
        "name": request.json["name"],
        "email": request.json["email"],
        "phone": request.json["phone"],
        "role": request.json["role"],
        "schedule": request.json["schedule"],
    }

    employees[new_id] = new_employee
    return jsonify({"success": f"{new_employee['name']} is added"}), 201


@employee_blueprint.route("/employees/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    """
    Update employee in database
    ---
    parameters:
      - name: employee
        in: body
        schema:
            id: employee
            properties:
                name:
                    type: string
                    description: The name of the employee to be added
                email:
                    type: string
                    description: The email of the employee to be added
                phone:
                    type: string
                    description: The phone of the employee to be added
                role:
                    type: number
                    description: The role of the employee to be added
                schedule:
                    type: string
                    description: The gender of the employee to be added
    responses:
        201:
            description: employee updated
        400:
            descrpition : No data provided
    """
    if employee_id not in employees:
        return jsonify({"error": "Employee not found"}), 404

    if not request.json:
        return jsonify({"error": "No data provided"}), 400

    current_employee = employees[employee_id]

    allowed_fields = ["name", "email", "phone", "role", "schedule"]

    if not all(key in allowed_fields for key in request.json):
        invalid_fields = [key for key in request.json if key not in allowed_fields]
        return (
            jsonify({"error": f"Invalid input: Non-allowed fields {invalid_fields}"}),
            400,
        )

    updates = {
        key: request.json.get(key, current_employee.get(key)) for key in allowed_fields
    }

    current_employee.update(updates)

    return jsonify({"success": f"{current_employee['name']} is updated"}), 201


@employee_blueprint.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    """
    Delete an employee by ID.
    ---
    parameters:
      - name: employee_id
        in: path
        type: integer
        required: true
        description: ID of the employee to delete
    responses:
      200:
        description: employee deleted successfully
      404:
        description: employee not found
    """
    if employee_id not in employees:
        return jsonify({"error": "employee not found"}), 404

    del employees[employee_id]

    return jsonify({"success": f"employee with ID {employee_id} deleted"}), 200
