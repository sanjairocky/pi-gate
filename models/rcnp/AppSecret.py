from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..Base import BaseModel
import os


class AppSecret(BaseModel):
    __tablename__ = 'app_secret'  # Name of the database table

    secret_id = Column(Integer, ForeignKey('secret.id'),
                       primary_key=True)
    app_id = Column(Integer, ForeignKey('app.id'),
                    primary_key=True)
    mount_path = Column(String(255), nullable=False, default='/')
    base_path = Column(String(100), nullable=False, default='/etc/secrets')
    target_name = Column(String(50), nullable=False, default='')
    env = Column(Boolean, default=True)

    secret = relationship('Secret')

    app = relationship('App', back_populates='secrets')

    @property
    def url(self):

        if self.mount_path.startswith('/'):
            mount = self.mount_path[1:]
        else:
            mount = self.mount_path

        return os.path.join(self.base_path, mount)

    @property
    def name(self):
        return self.target_name or self.secret.name

    def __repr__(self):
        return f'<AppSecret(secret_id={self.secret_id}, app_id="{self.app_id}", env="{self.env}")>'
