import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config():
    DEBUG=False
    TESTING=False
    SECRET_KEY=os.getenv('SECRET_KEY')

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS').split(','))

class DevelopmentConfig(Config):
    DEBUG=True

    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URI")

configuration = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}