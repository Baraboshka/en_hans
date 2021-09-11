from sqlalchemy import create_engine

from sqlalchemy.engine.base import Engine

from keys import MYSQL_PASSWORD


MYSQL_HOST = 'localhost'
MYSQL_USER = 'adam'
DB_NAME = 'en_hans'

dburi = (
    "mysql+mysqlconnector://" +
    f"{MYSQL_USER}" +
    f":{MYSQL_PASSWORD}" +
    f"@{MYSQL_HOST}" +
    f"/{DB_NAME}" +
    "?charset=utf8mb4&collation=utf8mb4_unicode_ci"
)

engine: Engine = create_engine(dburi, pool_recycle=28500)
