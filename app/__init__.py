from flask import Flask
import os
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

    from .errors import errors_bp
    app.register_blueprint(errors_bp)
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    return app