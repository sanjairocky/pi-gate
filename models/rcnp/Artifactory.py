from sqlalchemy import Column, Integer, String, Boolean
from ..Base import BaseModel


class Artifactory(BaseModel):
    __tablename__ = 'artifactory'  # Name of the database table

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    active = Column(Boolean, nullable=False, default=False)
    url = Column(String(255), nullable=False)

    def __repr__(self):
        return f'<Artifactory(id={self.id}, name="{self.name}", url="{self.url}")>'
