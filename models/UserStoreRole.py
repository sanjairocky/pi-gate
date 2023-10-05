from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship  # Import relationship from SQLAlchemy
from .Base import BaseModel


class UserStoreRole(BaseModel):
    __tablename__ = 'user_store_role'
    user_id = Column(Integer, ForeignKey('user.id'),
                     primary_key=True, nullable=False)
    store_id = Column(Integer, ForeignKey('store.id'),
                      primary_key=True, nullable=False)
    role_id = Column(Integer, ForeignKey('store_role.id'),
                     primary_key=True, nullable=False)

    # Define relationships
    user = relationship('User', backref='user_store_roles')
    store = relationship('Store', backref='user_store_roles')
    role = relationship('StoreRole', backref='user_store_roles')
