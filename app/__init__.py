from flask import Flask
import os
from config import configuration as config

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(config['development'])
    else:
        # load the test config if passed in
        app.config.from_object(config['testing'])

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/")

    return app