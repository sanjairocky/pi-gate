from sqlalchemy import Column, Integer, String
from .Base import BaseModel


class Category(BaseModel):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, unique=True)
    description = Column(String(50), nullable=False)
