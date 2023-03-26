from databases import Database
from sqlalchemy import create_engine,MetaData
from core.config import get_settings

database = Database(get_settings().database_url,)
metadata = MetaData()
engine = create_engine(
    get_settings().database_url,
)