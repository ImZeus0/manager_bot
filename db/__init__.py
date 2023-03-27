from .users import users
from .base import metadata,engine
from .expenses import expenses

metadata.create_all(bind=engine)