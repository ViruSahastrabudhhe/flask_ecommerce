from flask import Blueprint
from .models import db, User, Role, UserRole
from .enums import RoleTypes

seeders_bp = Blueprint('seed', __name__)

'''
    ordered list of seed commands you should run:
    1. roles
    2. admin-user
'''

@seeders_bp.cli.command('roles')
def seed_roles():
    Role.query.delete()

    role_names = [
        RoleTypes.ADMIN,
        RoleTypes.SELLER,
        RoleTypes.BUYER,
    ]

    for role_name in role_names:
        role = Role()
        role.name = role_name

        db.session.add(role)
        db.session.commit()

        print(f"Successfully created {role}!")

@seeders_bp.cli.command('admin-user')
def seed_admin_user():
    User.query.delete()

    user = User()
    user.email = 'test@example.com'
    user.first_name = 'Test'
    user.last_name = 'User'
    user.set_password('password')

    db.session.add(user)
    db.session.commit()

    user_role = UserRole()
    user_role.user_id = user.id
    user_role.role_id = 1

    db.session.add(user_role)
    db.session.commit()

    print(f"Successfully created admin user {user}!")
