from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .Base import BaseModel


class Order(BaseModel):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    txn_src = Column(Integer, nullable=False)
    created_by = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_on = Column(DateTime, nullable=False)
    updated_on = Column(DateTime, nullable=False)
    updated_by = Column(Integer, ForeignKey('user.id'), nullable=False)
    status_id = Column(Integer, ForeignKey('order_status.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    type_id = Column(Integer, ForeignKey('order_type.id'), nullable=False)
    comments = Column(String, nullable=False)
    store_id = Column(Integer, ForeignKey('store.id'), nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'), nullable=False)

    # Define relationships
    created_by_user = relationship('User', foreign_keys=[created_by])
    user = relationship('User', foreign_keys=[user_id])
    updated_by_user = relationship('User', foreign_keys=[updated_by])
    status = relationship('OrderStatus', backref='orders')
    type = relationship('OrderType', backref='orders')
    store = relationship('Store')
    address = relationship('Address')
