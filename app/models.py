from .extensions import db
from typing import List
import bcrypt
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import (
    Text,
    ForeignKey
)

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    store: Mapped["Store"] = relationship(back_populates="user")

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
    
class Product(db.Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float] = mapped_column(default=0)
    stock: Mapped[int] = mapped_column(default=0)
    description: Mapped[str] = mapped_column(Text, default='')
    store_id: Mapped[int] = mapped_column(ForeignKey('stores.id'))

    store: Mapped["Store"] = relationship(back_populates="products")

class Store(db.Model):
    __tablename__ = 'stores'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    address: Mapped[str] = mapped_column(default='')
    description: Mapped[str] = mapped_column(Text, default='')
    is_active: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    products: Mapped[List["Product"]] = relationship(back_populates="store")
    user: Mapped["User"] = relationship(back_populates="store")

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'address': self.address,
            'description': self.description,
            'is_active': self.is_active,
            'user_id': self.user_id
        }