from sqlalchemy import Column, Integer, ForeignKey
from ..Base import BaseModel


class ProjectSecret(BaseModel):
    __tablename__ = 'project_secret'  # Name of the database table

    secret_id = Column(Integer, ForeignKey('secret.id'),
                       primary_key=True)
    app_id = Column(Integer, ForeignKey('app.id'),
                    primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'),
                        primary_key=True)

    def __repr__(self):
        return f'<ProjectSecret(secret_id={self.secret_id}, app_id="{self.app_id}", project_id="{self.project_id}")>'
