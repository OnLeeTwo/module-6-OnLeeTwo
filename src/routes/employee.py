from flask import Blueprint, request, jsonify
from flasgger import swag_from
from repository.repository import employees
from services.employee import (
    add_employee_services,
    update_employee_services,
    delete_employee_services,
)

employee_blueprint = Blueprint("employees", __name__)


@employee_blueprint.route("/employees", methods=["GET"])
@swag_from("../docs/employee/get_employee.yml")
def get_employee():
    return jsonify(employees), 200


@employee_blueprint.route("/employees/<string:employee_id>", methods=["GET"])
@swag_from("../docs/employee/get_employee_by_id.yml")
def get_employee_by_id(employee_id):
    selected_employee = employees.get(employee_id)
    if selected_employee:
        return jsonify(selected_employee)
    return jsonify({"error": "employee id not found"}), 404


@employee_blueprint.route("/employees", methods=["POST"])
@swag_from("../docs/employee/add_employee.yml")
def add_employee():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    result = add_employee_services(data)
    return jsonify(result["response"]), result["status_code"]


@employee_blueprint.route("/employees/<string:employee_id>", methods=["PUT"])
@swag_from("../docs/employee/update_employee.yml")
def update_employee(employee_id):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if employee_id not in employees:
        return jsonify({"error": "Employee not found"}), 404

    result = update_employee_services(employee_id, data)
    return jsonify(result["response"]), result["status_code"]


@employee_blueprint.route("/employees/<string:employee_id>", methods=["DELETE"])
@swag_from("../docs/employee/delete_employee.yml")
def delete_employee(employee_id):
    if employee_id not in employees:
        return jsonify({"error": "Employee not found"}), 404

    result = delete_employee_services(employee_id)
    return jsonify(result["response"]), result["status_code"]
