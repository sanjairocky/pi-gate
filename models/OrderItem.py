from sqlalchemy import Column, Integer, Float, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from .Base import BaseModel


class OrderItem(BaseModel):
    __tablename__ = 'order_item'
    product_id = Column(Integer, ForeignKey('product.id'),
                        primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey('order.id'),
                      primary_key=True, nullable=False)
    quantity = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    s_gst = Column(DECIMAL, nullable=False)
    c_gst = Column(DECIMAL, nullable=False)

    # Define relationships
    product = relationship('Product', backref='order_items')
    order = relationship('Order', backref='order_items')
