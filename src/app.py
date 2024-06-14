from flask import Flask, jsonify
from routes.animal import animal_blueprint
from routes.employee import employee_blueprint
from routes.enclosure import enclosure_blueprint
from routes.feeding import feeding_blueprint
from routes.report import report_blueprint
from flasgger import Swagger

template = {
    "swagger": "2.0",
    "info": {
        "title": "Zoo Management",
        "description": "An API for simulating managing zoo operation",
        "version": "1.2.0",
    },
}

app = Flask(__name__)
app.register_blueprint(animal_blueprint)
app.register_blueprint(employee_blueprint)
app.register_blueprint(feeding_blueprint)
app.register_blueprint(report_blueprint)
app.register_blueprint(enclosure_blueprint)
swagger = Swagger(app, template=template)


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
