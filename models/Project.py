from sqlalchemy import Column, Integer, String
from .Base import BaseModel
from sqlalchemy.orm import relationship


class Project(BaseModel):
    __tablename__ = 'project'  # Name of the database table

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))

    apps = relationship('App', back_populates='project')

    def __repr__(self):
        return f'<Project(id={self.id}, name="{self.name}", description="{self.description}")>'
