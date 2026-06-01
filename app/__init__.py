import os
from flask import Flask, jsonify
from config import configuration as config
from .extensions import (
    migrate, cors, db, jwt
)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(config['development'])
    else:
        # load the test config if passed in
        app.config.from_object(config['testing'])

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)

    @app.route('/api/')
    def index():
        return jsonify({'message': 'Hello World!'}), 200
    
    @app.cli.command('init-db')
    def init_db():
        db.drop_all()
        db.create_all()
        db.session.commit()
        
        print("Successfully reset the database!")

    from .errors import errors_bp as error_handlers
    app.register_blueprint(error_handlers)
    from .seeders import seeders_bp as seed
    app.register_blueprint(seed)
    from .auth import auth_bp as auth_routes
    app.register_blueprint(auth_routes, url_prefix='/api/auth')
    from .admin import admin_bp as admin
    app.register_blueprint(admin, url_prefix='/api/admin')
    from .product import product_bp as products
    app.register_blueprint(products, url_prefix='/api/products')
    from .store import store_bp as stores
    app.register_blueprint(stores, url_prefix='/api/stores')
    from .address import address_bp as addresses
    app.register_blueprint(addresses, url_prefix='/api/addresses')

    return app