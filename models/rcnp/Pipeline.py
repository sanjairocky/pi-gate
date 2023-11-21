from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from ..Base import BaseModel
from sqlalchemy.orm import relationship


class Pipeline(BaseModel):
    __tablename__ = 'pipeline'  # Name of the database table

    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id = Column(Integer, ForeignKey('app.id'))
    artifactory_id = Column(Integer, ForeignKey('artifactory.id'))
    artifact = Column(String(255), nullable=False)
    version = Column(String(15), nullable=False, default='latest')
    build_skip = Column(Boolean, nullable=False, default=False)
    deploy_skip = Column(Boolean, nullable=False, default=False)
    active = Column(Boolean, nullable=False, default=True)
    log = Column(String, nullable=False)

    app = relationship('App', back_populates='pipelines')

    def __repr__(self):
        return f'<Pipeline(app_id={self.app_id}, ranAt="{self.created_on}", active={self.active})>'
