from .extensions import db, Base
from .enums import (
    RoleTypes, StoreAddressTypes,
    StoreStatusTypes
)
from typing import List
from zoneinfo import ZoneInfo
import bcrypt
import enum
from datetime import datetime
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

now = datetime.now(ZoneInfo("Asia/Manila"))

class UserRole(db.Model):
    __tablename__ = 'user_roles'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="roles")
    role: Mapped["Role"] = relationship(back_populates="users")

    def to_json(self):
        return {
            'name': f'{self.role.name.value}',
        }

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, onupdate=now)

    roles: Mapped[List["UserRole"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    addresses: Mapped[List["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    store: Mapped["Store"] = relationship(back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str):
        password = password.encode('utf-8')
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())

    def check_password(self, password: str):
        password = password.encode('utf-8')
        self.password = self.password.encode('utf-8')
        return bcrypt.checkpw(password, self.password)

    def __repr__(self) -> str:
        return f'ID: {self.id}, Email: {self.email}'
    
    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'roles': [role.to_json() for role in self.roles],
        }
    
class Role(db.Model):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[RoleTypes] = mapped_column(Enum(RoleTypes))

    def __repr__(self) -> str:
        return f'ID: {self.id}, Name: {self.name}'
    
    def to_json(self):
        return {
            'name': f'{self.name.value}',
        }
    
    users: Mapped[List["UserRole"]] = relationship(back_populates="role")

class Product(db.Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float, default=0)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    description: Mapped[str] = mapped_column(Text, default='')
    store_id: Mapped[int] = mapped_column(ForeignKey('stores.id', ondelete="CASCADE"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, onupdate=now)

    store: Mapped["Store"] = relationship(back_populates="products")

# class Category(db.Model):
#     __tablename__ = 'categories'

# class ProductCategory(db.Model):
#     __tablename__ = 'product_categories'

class Store(db.Model):
    __tablename__ = 'stores'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[StoreStatusTypes] = mapped_column(Enum(StoreStatusTypes), default=StoreStatusTypes.PENDING)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, onupdate=now)

    products: Mapped[List["Product"]] = relationship(back_populates="store")
    documents: Mapped["StoreDocuments"] = relationship(back_populates="store", cascade="all, delete-orphan")
    user: Mapped["User"] = relationship(back_populates="store")
    addresses: Mapped[List["StoreAddress"]] = relationship(back_populates="store", cascade="all, delete-orphan")  

    def is_approved(self):
        return self.status == StoreStatusTypes.APPROVED

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'address': [address.to_json() for address in self.addresses if address.is_active == True],
            'description': self.description,
            'is_active': self.is_active,
            'user_id': self.user_id
        }
    
class Address(db.Model):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    province: Mapped[str] = mapped_column(String(255), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[enum.Enum] = mapped_column(Enum('Shipping', 'Billing'), default='Shipping')
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="addresses")

    def to_json(self):
        return {
            'id': self.id,
            'country': self.country,
            'address': self.address,
            'city': self.city,
            'province': self.province,
            'zip_code': self.zip_code,
            'type': self.type,
            'is_active': self.is_active
        }

class StoreAddress(db.Model):
    __tablename__ = 'store_addresses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    province: Mapped[str] = mapped_column(String(255), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[StoreAddressTypes] = mapped_column(Enum(StoreAddressTypes))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    store_id: Mapped[int] = mapped_column(ForeignKey('stores.id', ondelete="CASCADE"))

    store: Mapped["Store"] = relationship(back_populates="addresses")

    def to_json(self):
        return {
            'id': self.id,
            'country': self.country,
            'address': self.address,
            'city': self.city,
            'province': self.province,
            'zip_code': self.zip_code,
            'type': self.type.value,
            'is_active': self.is_active
        }

class StoreDocuments(db.Model):
    __tablename__ = 'store_documents'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    valid_id: Mapped[str] = mapped_column(String(255))
    proof_of_address: Mapped[str] = mapped_column(String(255))
    business_registration_certificate: Mapped[str] = mapped_column(String(255))
    business_permit: Mapped[str] = mapped_column(String(255))
    bir_certificate: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    store_id: Mapped[int] = mapped_column(ForeignKey('stores.id', ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, onupdate=now)

    store: Mapped["Store"] = relationship(back_populates='documents')

    def to_json(self):
        return {
            'valid_id': self.valid_id,
            'proof_of_address': self.proof_of_address,
            'business_registration_certificate': self.business_registration_certificate,
            'business_permit': self.business_permit,
            'bir_certificate': self.bir_certificate,
            'user_id': self.user_id,
            'store_id': self.store.id
        }