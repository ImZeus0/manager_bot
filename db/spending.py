import sqlalchemy
from .base import metadata
import datetime

spending = sqlalchemy.Table(
    'spending',
    metadata,
    sqlalchemy.Column('id',sqlalchemy.Integer,primary_key=True,autoincrement=True,unique=True),
    sqlalchemy.Column('created_at',sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now()),
    sqlalchemy.Column('updated_at',sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now()),
    sqlalchemy.Column('spend',sqlalchemy.Float,unique=True),
    sqlalchemy.Column('id_agency', sqlalchemy.Integer, sqlalchemy.ForeignKey('agencys.id',ondelete='CASCADE'), nullable=False),
    sqlalchemy.Column('id_user', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id_user',ondelete='CASCADE'), nullable=False),
    sqlalchemy.Column('count_ban', sqlalchemy.Integer, nullable=False)
)