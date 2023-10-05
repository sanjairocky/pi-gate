from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .Base import BaseModel


class StoreRolePermission(BaseModel):
    __tablename__ = 'store_role_permission'
    role_id = Column(Integer, ForeignKey('store_role.id'),
                     primary_key=True, nullable=False)
    permission = Column(String(30), ForeignKey(
        'store_permission.name'), primary_key=True, nullable=False)

    # Define relationships
    role = relationship('StoreRole', backref='role_permissions')
    store_permission = relationship(
        'StorePermission', backref='permission_roles')
