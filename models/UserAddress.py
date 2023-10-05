from sqlalchemy import Column, Integer, ForeignKey
from .Base import BaseModel
from sqlalchemy.orm import relationship


class UserAddress(BaseModel):
    __tablename__ = 'user_address'
    user_id = Column(Integer, ForeignKey('user.id'),
                     primary_key=True, nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'),
                        primary_key=True, nullable=False)

    # Define relationships
    user = relationship('User', backref='user_addresses')
    address = relationship('Address', backref='user_addresses')
