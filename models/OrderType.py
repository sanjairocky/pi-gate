from sqlalchemy import Column, Integer, String
from .Base import BaseModel
from sqlalchemy.orm import relationship


class OrderType(BaseModel):
    __tablename__ = 'order_type'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(30), nullable=False)
    description = Column(String(50), nullable=False)

    # Define the relationship to Order with a backref
    orders = relationship('Order', backref='type')
