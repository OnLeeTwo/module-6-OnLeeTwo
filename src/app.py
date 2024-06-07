from flask import Flask, jsonify
from animal_view import animal_blueprint
from employee_view import employee_blueprint
from feeding_view import feeding_blueprint
from report_view import report_blueprint
from flasgger import Swagger


app = Flask(__name__)
app.register_blueprint(animal_blueprint)
app.register_blueprint(employee_blueprint)
app.register_blueprint(feeding_blueprint)
app.register_blueprint(report_blueprint)
swagger = Swagger(app)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Route not found"}), 404


@app.route("/")
def home():
    welcome_page = """<p>Welcome to the zoo API! Read the documentation in /apidocs for more information about how to use this API!</p>
    <p>Created by Owent Ovandy, 7 June 2024</p>"""

    return welcome_page


if __name__ == "__main__":
    app.run(debug=True)
