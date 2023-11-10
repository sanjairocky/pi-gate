from sqlalchemy import Column, Integer, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship
from ..Base import BaseModel


class Quota(BaseModel):
    __tablename__ = 'quota'  # Name of the database table

    id = Column(Integer,
                primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    cluster_id = Column(Integer, ForeignKey('cluster.id'), nullable=False)
    cpu = Column(Integer, nullable=False)
    memory = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False, unique=True)

    active = Column(Boolean, nullable=False, default=False)

    stages = relationship('Stage', back_populates='quota')

    cluster = relationship('Cluster', back_populates='quotas')

    project = relationship('Project', back_populates='quotas')

    def __repr__(self):
        return f'<Quota(name={self.name}, cluster="{self.cluster.name}", cpu="{self.cpu}", memory="{self.memory}", active={self.active})>'
