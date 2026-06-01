from . import product_bp
from flask import (
    jsonify
)

@product_bp.get('/')
def getProducts():
    return jsonify({'message': 'Hello World!'}), 200