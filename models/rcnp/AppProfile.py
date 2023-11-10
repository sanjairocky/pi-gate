from sqlalchemy import Column, Integer, String, Text
from ..Base import BaseModel


class AppProfile(BaseModel):
    __tablename__ = 'app_profile'  # Name of the database table

    app_id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, nullable=False, unique=True)
    order = Column(Integer)

    def __repr__(self):
        return f'<Profile(id={self.id}, name="{self.name}", description="{self.description}")>'
