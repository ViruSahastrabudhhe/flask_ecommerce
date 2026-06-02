from . import address_bp
from flask import (
    jsonify, request, abort, current_app
)
from flask_jwt_extended import (
    jwt_required,
    current_user,
)
from ..models import db, Address
from ..requests import CreateAddressRequest

@address_bp.get('/<int:id>')
def get_address_by_id(id: int):
    try:
        address = Address.query.filter_by(id=id).one_or_none()

        if address is None:
            return jsonify({'message': 'Address not found'}), 404
        
        return jsonify({'address': address.to_json()}), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching address with id {id}: {str(e)}")
        return jsonify({'message': 'Internal error'}), 500

@address_bp.get('/user')
@jwt_required()
def get_user_addresses():
    try:
        addresses = Address.query.filter_by(user_id=current_user.id).all()

        if addresses is None:
            return jsonify({'message': 'Address not found'}), 404

        return jsonify({'addresses': [address.to_json() for address in addresses]}), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching addresses with user id {current_user.id}: {str(e)}")
        return jsonify({'message': 'Internal error'}), 500

@address_bp.post('/create')
@jwt_required()
def create_address():
    if not request.is_json:
        abort(400)

    address_data = request.get_json()

    try:
        data = CreateAddressRequest(**address_data)
        country = data.country
        address_value = data.address
        city = data.city
        province = data.province
        zip_code = data.zip_code
        type = data.type
        is_active = data.is_active

        address = Address()
        address.country = country
        address.address = address_value
        address.city = city
        address.province = province
        address.zip_code = zip_code
        address.type = type
        address.is_active = is_active
        address.user_id = current_user.id

        db.session.add(address)
        db.session.commit()

        return jsonify({'message': 'Successfully created address!', 'address': address.to_json()}), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.info(f"Error creating address: {str(e)}")
        return jsonify({'message': 'Internal error'}), 500