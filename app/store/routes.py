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
from ..enums import StoreStatusTypes, RoleTypes
from ..decorators import admin_required
from ..models import (
    db, Store, StoreDocuments, StoreAddress,
    Role, UserRole
)
from ..requests import CreateStoreRequest
from werkzeug.utils import secure_filename

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

@store_bp.get('/')
def get_all_stores():
    try:
        stores = Store.query.limit(5)

        return jsonify({'stores': [store.to_json() for store in stores]}), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching all stores: {str(e)}")
        return jsonify({'message': 'Internal error'}), 500

@store_bp.put('/approve/<int:store_id>')
@jwt_required()
@admin_required()
def approve_store(store_id: int):
    try:
        store = Store.query.filter_by(id=store_id).one_or_none()

        if store is None:
            return jsonify({'message': f'Store with id {store_id} not found!'}), 404

        store.is_active = True
        store.status = StoreStatusTypes.APPROVED
        user_role = UserRole()
        user_role.role = Role.query.filter_by(name=RoleTypes.SELLER).one_or_none()
        store.user.roles.append(user_role)
        
        db.session.commit()

        return jsonify({'message': f'Store with id {store_id} has been activated!'}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error activating store with id {store_id}: {str(e)}")
        return jsonify({'message': 'Internal error'}), 500

@store_bp.post('/create')
@jwt_required()
def create_store():
    if not request.is_json:
        abort(400)

    create_data = request.get_json()

    try:
        data = CreateStoreRequest(**create_data)

        if not data.name or not data.email:
            return jsonify({'message': 'Please input the store name and email!'}), 400
        if Store.query.filter_by(email=data.email).first() is not None:
            return jsonify({'message': 'Store already exists!'}), 400

        store = Store()
        store.name = data.name
        store.email = data.email
        store.description = data.description
        store.user_id = current_user.id

        storeDocuments = StoreDocuments()
        storeDocuments.valid_id = data.valid_id
        storeDocuments.proof_of_address = data.proof_of_address
        storeDocuments.business_registration_certificate = data.business_registration_certificate
        storeDocuments.business_permit = data.business_permit
        storeDocuments.bir_certificate = data.bir_certificate
        storeDocuments.user_id = store.user_id
        storeDocuments.store_id = store.id

        store.documents = storeDocuments

        db.session.add(store)
        db.session.flush()

        storeAddress = StoreAddress()
        storeAddress.country = data.country
        storeAddress.address = data.address
        storeAddress.city = data.city
        storeAddress.province = data.province
        storeAddress.zip_code = data.zip_code
        storeAddress.type = data.type
        storeAddress.is_active = data.is_active
        storeAddress.user_id = store.user_id

        store.addresses.append(storeAddress)

        db.session.commit()

        return jsonify({'message': f'Successfully created store {store.name}!', 'store': store.to_json()}), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating store: {str(e)}")
        return jsonify({'message': 'Internal error'}), 500