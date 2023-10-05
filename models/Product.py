from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from .Base import BaseModel


class Product(BaseModel):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(100), nullable=False)
    barcode = Column(String, nullable=False, unique=True)
    mrp = Column(Float, nullable=False)
    unit_id = Column(Integer, nullable=False)
    quantity = Column(Float, nullable=False)

    unit = relationship('Unit')

    # Define the relationship to Inventory
    inventories = relationship('Inventory', backref='product')

    # Define a single backref for related products
    related_products = relationship(
        'RelatedProduct',
        primaryjoin="or_(Product.id == RelatedProduct.from_product_id, Product.id == RelatedProduct.to_product_id)"
    )
