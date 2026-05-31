from .extensions import db
from .enums import (
    RoleTypes
)
from typing import List
from zoneinfo import ZoneInfo
import bcrypt
import datetime

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import (
    String,
    Integer,
    Float,
    Boolean,
    Text,
    ForeignKey,
    DateTime,
    Enum,
)

now = datetime.datetime.now(ZoneInfo("Asia/Manila"))

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=now)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True, onupdate=now)

    roles: Mapped[List["UserRole"]] = relationship(back_populates="user", cascade="all")
    store: Mapped["Store"] = relationship(back_populates="user", cascade="all")

    def set_password(self, password):
        password = password.encode('utf-8')
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())

    def check_password(self, password):
        password = password.encode('utf-8')
        return bcrypt.checkpw(password, self.password)

    def __repr__(self) -> str:
        return f'ID: {self.id}, Email: {self.email}'
    
    def to_json(self):
        return {
            'id': self.id,
            'email': self.email
        }
    
class Role(db.Model):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[RoleTypes] = mapped_column(Enum(RoleTypes))

    def __repr__(self) -> str:
        return f'ID: {self.id}, Name: {self.name}'

class UserRole(db.Model):
    __tablename__ = 'user_roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    assigned_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=now)

    user: Mapped["User"] = relationship(back_populates="roles", cascade="all")
    role: Mapped["Role"] = relationship(cascade="all")

class Product(db.Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float, default=0)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    description: Mapped[str] = mapped_column(Text, default='')
    store_id: Mapped[int] = mapped_column(ForeignKey('stores.id'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=now)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True, onupdate=now)

    store: Mapped["Store"] = relationship(back_populates="products")

class Store(db.Model):
    __tablename__ = 'stores'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    address: Mapped[str] = mapped_column(String(100), default='')
    description: Mapped[str] = mapped_column(Text, default='')
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=now)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True, onupdate=now)

    products: Mapped[List["Product"]] = relationship(back_populates="store", cascade="all")
    user: Mapped["User"] = relationship(back_populates="store", cascade="all")

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