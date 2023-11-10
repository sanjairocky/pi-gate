from sqlalchemy import Column, Integer, String
from ..Base import BaseModel


class Secret(BaseModel):
    __tablename__ = 'secret'  # Name of the database table

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    value = Column(String(1000))

    def __repr__(self):
        return f'<Secret(id={self.id}, name="{self.name}", value="{self.value}")>'
