from . import store_bp
from flask import (
    request,
    jsonify,
    abort,
    current_app,
)
from flask_jwt_extended import (
    jwt_required,
    current_user,
)
from ..models import db, Store
from ..requests import CreateStoreRequest

@store_bp.get('/<int:id>')
def get_store_by_id(id: int):
    try:
        store = Store.query.filter_by(id=id).one_or_none()

        if store is None:
            return jsonify({'message': f'Store with id {id} not found!'}), 404

        return jsonify({'store': store.to_json()}), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching store with id {id}: {str(e)}")
        return jsonify({'message': 'Internal error'}), 500
    
@store_bp.post('/create')
@jwt_required()
def create_store():
    if not request.is_json:
        abort(400)

    create_data = request.get_json()

    try:
        data = CreateStoreRequest(**create_data)
        name = data.name
        email = data.email
        description = data.description

        if not name or not email:
            return jsonify({'message': 'Please input the store name and email!'}), 400
        if Store.query.filter_by(email=email).first() is not None:
            return jsonify({'message': 'Store already exists!'}), 400

        store = Store()
        store.name = name
        store.email = email
        store.description = description
        store.user_id = current_user.id

        db.session.add(store)
        db.session.commit()

        return jsonify({'message': f'Successfully created store {store.name}!'}), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating store: {str(e)}")
        return jsonify({'message': 'Internal error'}), 500