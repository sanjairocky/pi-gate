from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .Base import BaseModel
from sqlalchemy.orm import relationship


class Cluster(BaseModel):
    __tablename__ = 'cluster'  # Name of the database table

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    active = Column(Boolean, nullable=False, default=False)
    cpu = Column(Integer)
    memory = Column(Integer)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

    region = relationship('Region', back_populates='clusters')

    quotas = relationship('Quota', back_populates='cluster')

    def __repr__(self):
        return f'<Cluster(id={self.id}, name="{self.name}", region={self.region.name}, description="{self.description}")>'
