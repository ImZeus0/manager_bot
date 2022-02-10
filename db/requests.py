import sqlalchemy
from .base import metadata
import datetime

requests = sqlalchemy.Table(
    'requests',
    metadata,
    sqlalchemy.Column('id',sqlalchemy.Integer,primary_key=True,autoincrement=True,unique=True),
    sqlalchemy.Column('created_at',sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now()),
    sqlalchemy.Column('updated_at',sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now()),
    sqlalchemy.Column('name',sqlalchemy.String,unique=True),
    sqlalchemy.Column('id_agency', sqlalchemy.Integer, sqlalchemy.ForeignKey('agencys.id',ondelete='CASCADE'), nullable=False)
)