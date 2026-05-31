from flask import Blueprint

stores_bp = Blueprint('stores', __name__)

from . import routes