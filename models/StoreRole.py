from sqlalchemy import Column, Integer, String
from .Base import BaseModel
from sqlalchemy.orm import relationship


class StoreRole(BaseModel):
    __tablename__ = 'store_role'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(9), nullable=False, unique=True)
    description = Column(String(50), nullable=False)

    # Define relationships
    role_permissions = relationship('StoreRolePermission', backref='role')
