import os
from flask import Flask
from flask_smorest import Api
from source.db import db
from source.resources.sentence import sentblueprint as SentenceBlueprint

def create_app():
    # creates an application instance app using Flask() class
    app = Flask(__name__)

    # swagger documentation details
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Employee Crud Example"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    basedir = os.path.abspath(os.path.dirname(__file__))

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Connect the database to the app instance
    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()

    #register employee blueprint
    api.register_blueprint(SentenceBlueprint)

    return app