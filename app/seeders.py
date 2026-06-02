from flask import Blueprint
from .models import (
    db, User, Role, UserRole, Store
)
from .enums import RoleTypes

seeders_bp = Blueprint('seed', __name__)

@seeders_bp.cli.command('db')
def init_db():
    db.drop_all()
    db.create_all()
    seed_roles()
    seed_admin_user()
    db.session.commit()
    
    print("Successfully initialized and seeded the database!")

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

    print(f"Successfully created roles!")

def seed_admin_user():
    user = User()
    user_role = UserRole()
    user_role.role = Role.query.filter_by(name=RoleTypes.ADMIN).one_or_none()

    user.email = 'test@example.com'
    user.first_name = 'Test'
    user.last_name = 'User'
    user.set_password('password')
    user.roles.append(user_role)

    db.session.add(user)
    db.session.commit()

    print(f"Successfully created admin user {user.email}!")

def seed_stores():
    pass