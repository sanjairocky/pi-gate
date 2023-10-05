from sqlalchemy import Column, Integer, String, create_engine
from .Base import BaseModel


class Address(BaseModel):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String(120), nullable=False)
    description = Column(String(50))
    lat = Column(Integer)
    long = Column(Integer)
    map_loc = Column(String(100))
    name = Column(String(10), nullable=False)
