from . import admin_bp
from flask import (
    jsonify,
    request
)
from flask_jwt_extended import (
    jwt_required,
    current_user,
)
from ..models import db, User
from ..decorators import admin_required

@admin_bp.get('/users')
@jwt_required()
@admin_required()
def get_users():
    users = User.query.all()
    return jsonify([user.to_json() for user in users]), 200