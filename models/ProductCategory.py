from sqlalchemy import Column, Integer, String, ForeignKey
from .Base import BaseModel
from sqlalchemy.orm import relationship


class ProductCategory(BaseModel):
    __tablename__ = 'product_category'
    catagory_id = Column(Integer, ForeignKey('category.id'),
                         primary_key=True, nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'),
                        primary_key=True, nullable=False)
    comments = Column(String(50), nullable=False)

    # Define relationship to Category
    category = relationship('Category', backref='category_products')

    # Define relationship to Product
    product = relationship('Product', backref='product_categories')
