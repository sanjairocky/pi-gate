from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from ..Base import BaseModel
from sqlalchemy.orm import relationship


class Pipeline(BaseModel):
    __tablename__ = 'pipeline'  # Name of the database table

    app_id = Column(Integer, ForeignKey('app.id'),
                    primary_key=True)
    artifactory_id = Column(Integer, ForeignKey('artifactory.id'))
    artifact = Column(String(255), nullable=False, unique=True)
    version = Column(String(15), nullable=False, default='latest')
    build_skip = Column(Boolean, nullable=False, default=False)
    deploy_skip = Column(Boolean, nullable=False, default=False)
    active = Column(Boolean, nullable=False, default=True)
    log = Column(String, nullable=False)

    def __repr__(self):
        return f'<Project(id={self.id}, name="{self.name}", active={self.active}, description="{self.description}")>'
