import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    DEBUG=True
    SECRET_KEY=os.getenv('SECRET_KEY')

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI")
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

configuration = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}