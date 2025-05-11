from flask import Blueprint

mqtt_bp = Blueprint('mqtt', __name__)

from . import routes