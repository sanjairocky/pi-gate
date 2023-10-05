from sqlalchemy import Column, Integer, String
from .Base import BaseModel


class StoreTransactionType(BaseModel):
    __tablename__ = 'store_transaction_type'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(10), nullable=False, unique=True)
    description = Column(String(50), nullable=False)
