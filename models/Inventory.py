from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from .Base import BaseModel


class Inventory(BaseModel):
    __tablename__ = 'inventory'
    product_id = Column(Integer, primary_key=True)
    store_id = Column(Integer, primary_key=True)
    quantity = Column(Float(1000), nullable=False)
    cost_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    updated_by = Column(Integer, nullable=False)
    updated_on = Column(DateTime, nullable=False)

    # Define relationships
    product = relationship('Product', backref='inventories')
    store = relationship('Store', backref='inventories')
    updated_by_user = relationship('User')
