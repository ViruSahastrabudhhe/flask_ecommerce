from functools import wraps

from flask import (
    jsonify
)
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt
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