from . import auth_bp
from flask import jsonify

@auth_bp.get('/')
def index():
    return jsonify({"message": "Hello, World!"})