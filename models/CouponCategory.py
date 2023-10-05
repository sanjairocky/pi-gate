from sqlalchemy import Column, Integer, String, ForeignKey
from .Base import BaseModel
from sqlalchemy.orm import relationship


class CouponCategory(BaseModel):
    __tablename__ = 'coupon_category'
    category_id = Column(Integer, ForeignKey('category.id'),
                         primary_key=True, nullable=False)
    coupon_id = Column(String(15), ForeignKey('coupon.id'),
                       primary_key=True, nullable=False)

    # Define relationships
    category = relationship('Category', backref='coupon_categories')
    coupon = relationship('Coupon', backref='coupon_categories')
