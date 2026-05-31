from .extensions import db
import bcrypt
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    def set_password(self, password):
        password = password.encode('utf-8')
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())

    def check_password(self, password):
        password = password.encode('utf-8')
        return bcrypt.checkpw(password, self.password)

    def __repr__(self):
        return f'ID: {self.id}, Email: {self.email}'
    
    def to_json(self):
        return {
            'id': self.id,
            'email': self.email
        }