import os

from flask import Flask, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from flask._compat import string_types

from config import configs

db = SQLAlchemy()


def create_app(config_name):
    application = Flask(__name__)

    application.config['NOTIFY_API_ENVIRONMENT'] = config_name
    application.config.from_object(configs[config_name])

    db.init_app(application)
    init_app(application)

    from .main import main as main_blueprint
    application.register_blueprint(main_blueprint)

    return application


def init_app(app):
    for key, value in app.config.items():
        if key in os.environ:
            app.config[key] = convert_to_boolean(os.environ[key])


def convert_to_boolean(value):
    if isinstance(value, string_types):
        if value.lower() in ['t', 'true', 'on', 'yes', '1']:
            return True
        elif value.lower() in ['f', 'false', 'off', 'no', '0']:
            return False

    return value
