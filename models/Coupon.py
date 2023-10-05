from sqlalchemy import Column, String, Integer
from .Base import BaseModel


class Coupon(BaseModel):
    __tablename__ = 'coupon'
    id = Column(String(15), primary_key=True, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    percent = Column(Integer, nullable=False)
