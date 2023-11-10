from sqlalchemy import Column, Integer, String, Text
from ..Base import BaseModel


class Profile(BaseModel):
    __tablename__ = 'profile'  # Name of the database table

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(1000))
    config = Column(Text)

    def __repr__(self):
        return f'<Profile(id={self.id}, name="{self.name}", description="{self.description}")>'
