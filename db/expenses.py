import sqlalchemy
from .base import metadata
import datetime
from core.enums import Operation,Status
expenses = sqlalchemy.Table(
    'expenses',
    metadata,
    sqlalchemy.Column('id',sqlalchemy.Integer,primary_key=True,autoincrement=True,unique=True),
    sqlalchemy.Column('created_at',sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now()),
    sqlalchemy.Column('updated_at',sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now()),
    sqlalchemy.Column('type_operation',sqlalchemy.Enum(Operation)),
    sqlalchemy.Column('id_user', sqlalchemy.Integer),
    sqlalchemy.Column('service', sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column('amount', sqlalchemy.Float, nullable=False),
    sqlalchemy.Column('currency', sqlalchemy.String(20), nullable=False),
    sqlalchemy.Column('purpose', sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column('payment_key', sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column('status', sqlalchemy.Enum(Status), nullable=False),

)