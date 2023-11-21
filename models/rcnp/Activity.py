from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..Base import BaseModel


class Activity(BaseModel):
    __tablename__ = 'activity'  # Name of the database table

    description = Column(String(1000))
    project_id = Column(Integer, ForeignKey('project.id'),
                        nullable=False, primary_key=True)
    app_id = Column(Integer, ForeignKey('app.id'),
                    nullable=False, primary_key=True)
    event = Column(String(255), nullable=False)

    project = relationship('Project', back_populates='activities')

    app = relationship('App', back_populates='activities')
