from functools import wraps

from flask import (
    jsonify
)
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt,
    current_user
)
from .models import (
    Store
)
from .enums import (
    StoreStatusTypes
)

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['is_admin']:
                return fn(*args, **kwargs)
            
            return jsonify({'message': 'Admins only!'}), 403
        return decorator
    return wrapper

def seller_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['is_seller']:
                return fn(*args, **kwargs)
            
            return jsonify({'message': 'Sellers only!'}), 403
        return decorator
    return wrapper

def is_store_approved():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            store=Store.query.filter_by(user_id=current_user.id).one_or_none()
            if store.is_approved():
                return fn(*args, **kwargs)
            else:
                return jsonify({"message": "Store must be accepted first!"}), 403
        return decorator
    return wrapper