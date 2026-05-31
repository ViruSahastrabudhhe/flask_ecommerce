from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

migrate=Migrate()
cors=CORS()
jwt=JWTManager()

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)