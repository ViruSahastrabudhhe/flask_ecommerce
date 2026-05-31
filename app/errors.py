from flask import (
    Blueprint,
    jsonify
)
from .models import db
from pydantic import ValidationError

errors_bp = Blueprint('errors', __name__)

@errors_bp.app_errorhandler(400)
def bad_request_error(error):
    return jsonify({'message': 'Bad request'}), 400

@errors_bp.app_errorhandler(404)
def not_found_error(error):
    return jsonify({'message': 'Not found'}), 404

@errors_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'message': 'Internal error'}), 500

@errors_bp.app_errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({
        "message": "Validation Error",
        "details": e.errors()
    }), 400