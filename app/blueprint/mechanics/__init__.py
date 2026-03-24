from flask import Blueprint

mechanics_bp = Blueprint('mechanics', __name__)

from .routes import *
from .schemas import *
