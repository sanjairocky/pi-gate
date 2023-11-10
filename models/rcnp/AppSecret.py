from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from ..Base import BaseModel


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

    def __repr__(self):
        return f'<AppSecret(secret_id={self.secret_id}, app_id="{self.app_id}", env="{self.env}")>'
