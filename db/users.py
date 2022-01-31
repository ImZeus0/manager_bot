import sqlalchemy
from .base import metadata
import datetime

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id',sqlalchemy.Integer,primary_key=True,autoincrement=True,unique=True),
    sqlalchemy.Column('id_user',sqlalchemy.BigInteger),
    sqlalchemy.Column('nickname',sqlalchemy.String,unique=True,nullable=True),
    sqlalchemy.Column('created_at',sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now()),
    sqlalchemy.Column('updated_at',sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now()),
    sqlalchemy.Column('role',sqlalchemy.String,default='user'))