import click
from flask import Blueprint
from .models import db, User

seeders_bp = Blueprint('seeders', __name__)

@seeders_bp.cli.command('seed-user')
def seed_users():
    User.query.delete()

    user = User()
    user.email = 'test@example.com'
    user.first_name = 'Test'
    user.last_name = 'User'
    user.set_password('password')

    db.session.add(user)
    db.session.commit()