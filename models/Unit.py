from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import relationship
from .Base import BaseModel


class Unit(BaseModel):
    __tablename__ = 'unit'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(20), nullable=False, unique=True)
    description = Column(String(50), nullable=False)
