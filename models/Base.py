from sqlalchemy.orm import DeclarativeBase
from models.mixin import AuditMixin, ImportMixin
from datetime import datetime
from utils.db import gen_session


class class_property(object):

    # This class property is inspired from the behaviour of flaskSqlAlchemy
    # The behaviour of querying directly a model User.query.. is nice, but
    # the flaskSqlAlchemy dependency is not, so the behaviour is reproduced
    # with this trick of class property
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, _, owner_cls):
        return self.fget(owner_cls)


class Model(DeclarativeBase):
    __abstract__ = True

    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)
        self.creation_timestamp = datetime.utcnow()

    @classmethod
    def exists(cls, uid):
        return cls.get_by_id(uid) is not None

    @classmethod
    def all(cls):
        return cls.session.query(cls).all()

    @classmethod
    def delete_all(cls):
        cls.session.query(cls).delete()
        cls.session.commit()

    def delete(self):
        self.session.delete(self)
        self.session.commit()

    @classmethod
    def get_by_id(cls, uid):
        return cls.session.query(cls).get(uid)

    @classmethod
    def get_by_ids(cls, ids):
        pk_attr = getattr(cls, cls.get_primary_key_name())
        return cls.session.query.filter(pk_attr.in_(ids)).all()

    @classmethod
    def get_or_create(cls, uid=None, **kwargs):
        uid = uid or kwargs.get(cls.get_primary_key_name())
        instance = cls.get_by_id(uid) if uid else None
        if not instance:
            instance = cls.create(uid=uid, **kwargs)
        return instance

    @classmethod
    def get_primary_key_name(cls):
        return cls.inspect(cls).primary_key[0].name

    @classmethod
    def create_instance(cls, uid, **kwargs):
        if uid:
            kwargs[cls.get_primary_key_name()] = uid
        instance = cls(**kwargs)
        instance.creation_timestamp = datetime.utcnow()
        instance.save()
        return instance

    def get_id(self):
        pk = self.get_primary_key_name()
        return getattr(self, pk)

    def save(self):
        self.session.add(self)
        self.session.commit()
        return self

    @class_property
    def query(cls):
        return cls.session.query(cls)

    @class_property
    def session(cls):
        return gen_session()


class BaseModel(Model, AuditMixin, ImportMixin):
    __abstract__ = True
