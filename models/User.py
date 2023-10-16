from sqlalchemy import Column, Integer, String, Float, DateTime, DECIMAL, create_engine
from sqlalchemy.orm import relationship
from .Base import BaseModel


class User(BaseModel):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False, unique=True)
    mobile = Column(String(10), nullable=False, unique=True)

    # Define relationships
    # user_store_roles = relationship('UserStoreRole', backref='user')
    # user_addresses = relationship('UserAddress', backref='user')
