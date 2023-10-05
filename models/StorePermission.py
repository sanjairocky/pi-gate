from sqlalchemy import Column, String
from .Base import BaseModel
from sqlalchemy.orm import relationship


class StorePermission(BaseModel):
    __tablename__ = 'store_permission'
    name = Column(String(30), primary_key=True, nullable=False, unique=True)
    description = Column(String(100), nullable=False)

# Define the relationship to StoreRolePermission
    permission_roles = relationship(
        'StoreRolePermission', backref='store_permission')
