from sqlalchemy import Column, Integer, ForeignKey
from .Base import BaseModel


class RelatedProduct(BaseModel):
    __tablename__ = 'related_product'
    from_product_id = Column(Integer, ForeignKey(
        'product.id'), primary_key=True, nullable=False)
    to_product_id = Column(Integer, ForeignKey(
        'product.id'), primary_key=True, nullable=False)
