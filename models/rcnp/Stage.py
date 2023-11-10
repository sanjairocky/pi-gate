from sqlalchemy import Column, Integer, String, ForeignKey
from ..Base import BaseModel
from sqlalchemy.orm import relationship


class Stage(BaseModel):
    __tablename__ = 'stage'  # Name of the database table

    app_id = Column(Integer, ForeignKey('app.id'), primary_key=True)
    quota_id = Column(Integer, ForeignKey('quota.id'), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    c_names = Column(String(255))
    refs = Column(String(255), nullable=False)

    app = relationship('App', back_populates='stages')

    quota = relationship('Quota', back_populates='stages')
