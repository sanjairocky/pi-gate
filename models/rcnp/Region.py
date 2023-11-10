from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship
from ..Base import BaseModel


class Region(BaseModel):
    __tablename__ = 'region'  # Name of the database table

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    country = Column(String(2), nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    clusters = relationship('Cluster', back_populates='region')

    def __repr__(self):
        return f'<Region(name="{self.name}, "clusters="{len(self.clusters)}")>'
