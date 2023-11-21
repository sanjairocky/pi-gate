from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..Base import BaseModel
import uuid


class App(BaseModel):
    __tablename__ = 'app'  # Name of the database table

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    repository_url = Column(String(255))
    config_file = Column(String(50), default='rncp.yml')
    active = Column(Boolean, nullable=False, default=True)
    api_key = Column(String(36), nullable=False,
                     default=lambda: str(uuid.uuid4()))
    release_refs = Column(String(255), nullable=False, default='main')

    project = relationship('Project', back_populates='apps')

    stages = relationship('Stage', back_populates='app')

    activities = relationship('Activity', back_populates='app')

    project_secrets = relationship('ProjectSecret', back_populates='app')

    secrets = relationship('AppSecret', back_populates='app')

    pipelines = relationship('Pipeline', back_populates='app')
