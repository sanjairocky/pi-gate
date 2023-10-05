from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .Base import BaseModel


class Store(BaseModel):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False, unique=True)
    description = Column(String(100), nullable=False)
    parent_id = Column(Integer, nullable=False)
    address_id = Column(Integer, nullable=False)
    created_by = Column(Integer, nullable=False)
    # Define relationships
    parent = relationship('Store', remote_side=[id])
    address = relationship('Address')
    created_by_user = relationship('User')

    # Define the relationship to Inventory
    inventories = relationship('Inventory', backref='store')
    # Define the relationship to UserStoreRole
    user_store_roles = relationship('UserStoreRole', backref='store')
