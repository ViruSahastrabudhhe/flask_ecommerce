import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config():
    DEBUG=False
    SECRET_KEY=os.getenv('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG=True

    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URI")
    TESTING = True

configuration = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}