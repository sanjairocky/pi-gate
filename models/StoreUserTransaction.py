from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .Base import BaseModel


class StoreUserTransaction(BaseModel):
    __tablename__ = 'store_user_transaction'
    store_id = Column(Integer, ForeignKey('store.id'),
                      primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'),
                     primary_key=True,  nullable=False)
    amount = Column(Integer, nullable=False)
    comments = Column(String, nullable=False)
    transaction_type_id = Column(Integer, ForeignKey(
        'store_transaction_type.id'), nullable=False)

    # Define relationships
    store = relationship('Store', backref='user_transactions')
    user = relationship('User', backref='store_transactions')
    transaction_type = relationship(
        'StoreTransactionType', backref='user_transactions')
