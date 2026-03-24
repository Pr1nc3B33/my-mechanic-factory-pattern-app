from flask import Flask

from app.blueprint.customers import customers_bp
from app.extensions import ma
from app.models import db


def create_app(config_name='DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(customers_bp, url_prefix='/customers')

    return app
