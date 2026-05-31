from . import products_bp
from flask import (
    jsonify
)

@products_bp.get('/')
def getProducts():
    return jsonify({'message': 'Hello World!'}), 200