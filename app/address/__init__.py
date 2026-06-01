from flask import Blueprint

address_bp = Blueprint('addresses', __name__)

from . import routes