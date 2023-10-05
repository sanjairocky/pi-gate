from sqlalchemy import Column, Integer, ForeignKey
from .Base import BaseModel
from sqlalchemy.orm import relationship


class UserStoreDue(BaseModel):
    __tablename__ = 'user_store_due'
    user_id = Column(Integer, ForeignKey('user.id'),
                     primary_key=True, nullable=False)
    store_id = Column(Integer, ForeignKey('store.id'),
                      primary_key=True, nullable=False)
    amount = Column(Integer, nullable=False)

    # Define relationships
    user = relationship('User', backref='store_due')
    store = relationship('Store', backref='user_due')
