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
    
@address_bp.post('/create')
def create_address():
    if not request.is_json:
        abort(400)

    address_data = request.get_json()

    try:
        data = CreateAddressRequest(**address_data)
        country = data.country
        address = data.address
        city = data.city
        province = data.province
        zip_code = data.zip_code
        type = data.type
        is_active = data.is_active

    except Exception as e:
        current_app.logger.info(f"Error creating address: {str(e)}")
        return jsonify({'message': 'Internal error'}), 500