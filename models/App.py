from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .Base import BaseModel


class App(BaseModel):
    __tablename__ = 'app'  # Name of the database table

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    repository_url = Column(String(255))
    build_type = Column(String(50))

    project = relationship('Project', back_populates='apps')
