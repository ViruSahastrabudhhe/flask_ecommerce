from . import auth_bp
from flask import (
    request,
    abort,
    jsonify,
    current_app,
)
from ..extensions import jwt
from ..models import (
    db, User, UserRole
)
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    current_user,
)
from ..requests import (
    LoginUserRequest, RegisterUserRequest
)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return str(user.id)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

@auth_bp.post('/register')
def register():
    if not request.is_json:
        abort(400)

    register_data = request.get_json()

    try:
        data = RegisterUserRequest(**register_data)
        email = data.email
        first_name = data.first_name
        last_name = data.last_name
        password = data.password.get_secret_value()
        confirm_password = data.confirm_password.get_secret_value()

        if not email or not password or not confirm_password:
            return jsonify({'message': 'Please input your credentials!'}), 400
        if password != confirm_password:
            return jsonify({'message': 'Passwords do not match!'}), 400
        if User.query.filter_by(email=email).first() is not None:
            return jsonify({'message': 'Email already exists!'}), 400

        user = User()
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        db.session.flush()

        user_role = UserRole()
        user_role.user_id = user.id
        user_role.role_id = 3

        db.session.add(user_role)
        db.session.commit()

        return jsonify({"message": f"Successfully registered user {email}!"}), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error registering user with email {email}: {str(e)}")
        return jsonify({'message': 'Internal error'}), 500
    
@auth_bp.post('/login')
def login():
    if not request.is_json:
        abort(400)

    login_data = request.get_json()

    try:
        data = LoginUserRequest(**login_data)
        email = data.email
        password = data.password.get_secret_value()

        if not email or not password:
            return jsonify({'message': 'Please input your credentials!'}), 400

        user = User.query.filter_by(email=email).one_or_none()

        if user is None:
            return jsonify({'message': 'User does not exist!'}), 401
        if user.check_password(password)==False:
            return jsonify({'message': 'Incorrect password!'}), 401 
        
        access_token = create_access_token(identity=user)
        response = jsonify(message="Successfully logged in!", access_token=access_token)
        
        return response, 200
    except Exception as e:
        current_app.logger.error(f"Error logging in user with email {email}: {str(e)}")
        return jsonify({'message': 'Internal error'}), 500
    
@auth_bp.get('/protected')
@jwt_required()
def protected():
    return jsonify({
        'id': current_user.id,
        'message': 'This is a protected route!',
        'user': current_user.to_json()
    }), 200