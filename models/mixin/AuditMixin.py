from flask import g
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime
)
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship


class AuditMixin(object):
    """
        AuditMixin
        Mixin for models, adds 4 columns to stamp,
        time and user on creation and modification
        will create the following columns:

        :created on:
        :changed on:
        :created by:
        :changed by:
    """

    created_on = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    changed_on = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    @declared_attr
    def created_by_fk(cls):
        return Column(
            Integer, ForeignKey("user.id"), default=cls.get_user_id, nullable=False
        )

    @declared_attr
    def created_by(cls):
        return relationship(
            "User",
            primaryjoin="%s.created_by_fk == User.id" % cls.__name__,
            enable_typechecks=False,
        )

    @declared_attr
    def changed_by_fk(cls):
        return Column(
            Integer,
            ForeignKey("user.id"),
            default=cls.get_user_id,
            onupdate=cls.get_user_id,
            nullable=False,
        )

    @declared_attr
    def changed_by(cls):
        return relationship(
            "User",
            primaryjoin="%s.changed_by_fk == User.id" % cls.__name__,
            enable_typechecks=False,
        )

    @classmethod
    def get_user_id(cls):
        try:
            return 1
        except Exception:
            return None
