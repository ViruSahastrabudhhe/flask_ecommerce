from . import auth_bp

@auth_bp.get('/')
def index():
    return "Hello World!"