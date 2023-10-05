from sqlalchemy import Column, Integer, String, ForeignKey
from .Base import BaseModel
from sqlalchemy.orm import relationship


class ProductTag(BaseModel):
    __tablename__ = 'product_tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    name = Column(String(100), nullable=False)

    # Define relationship to Product
    product = relationship('Product', backref='product_tags')
