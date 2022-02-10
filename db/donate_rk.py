import sqlalchemy
from .base import metadata
import datetime

donate_rk = sqlalchemy.Table(
    'donate_rk',
    metadata,
    sqlalchemy.Column('id',sqlalchemy.Integer,primary_key=True,autoincrement=True,unique=True),
    sqlalchemy.Column('created_at',sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now()),
    sqlalchemy.Column('updated_at',sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now()),
    sqlalchemy.Column('ammount',sqlalchemy.Integer),
    sqlalchemy.Column('id_agency', sqlalchemy.Integer, sqlalchemy.ForeignKey('agencys.id',ondelete='CASCADE'), nullable=False),
    sqlalchemy.Column('email',sqlalchemy.String),
    sqlalchemy.Column('id_user', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id_user',ondelete='CASCADE'), nullable=False),
    sqlalchemy.Column('admin', sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column('cabinets', sqlalchemy.String, nullable=False),
    sqlalchemy.Column('status', sqlalchemy.String, nullable=False)
)