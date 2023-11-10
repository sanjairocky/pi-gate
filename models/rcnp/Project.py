from sqlalchemy import Column, Integer, String, Boolean
from ..Base import BaseModel
from sqlalchemy.orm import relationship
import uuid


class Project(BaseModel):
    __tablename__ = 'project'  # Name of the database table

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(1000))
    active = Column(Boolean, nullable=False, default=True)
    api_key = Column(String(36), nullable=False,
                     default=lambda: str(uuid.uuid4()))

    apps = relationship('App', back_populates='project')

    quotas = relationship('Quota', back_populates='project')

    def __repr__(self):
        return f'<Project(id={self.id}, name="{self.name}", active={self.active}, description="{self.description}")>'
