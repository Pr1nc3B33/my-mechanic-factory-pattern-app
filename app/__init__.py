from flask import Flask

from app.blueprint.customers import customers_bp
from app.blueprint.mechanics import mechanics_bp
from app.blueprint.service_tickets import service_tickets_bp
from app.blueprint.inventory import inventory_bp
from app.extensions import ma
from app.models import db
from .extensions import ma, limiter, cache

from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs' 
API_URL = '/static/swagger.yaml'


swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name':"MyMechanic API"
    }
)

def create_app(config_name='DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service-tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
