from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

from sqlalchemy_utils import database_exists, create_database

from src.constants import POSTGRESQL_HOST, POSTGRESQL_USER, POSTGRESQL_PASS, POSTGRESQL_PORT, POSTGRESQL_DB

drivername="postgresql+psycopg2"
host=POSTGRESQL_HOST
username=POSTGRESQL_USER
password=POSTGRESQL_PASS
port=POSTGRESQL_PORT
database=POSTGRESQL_DB

def connection():
    sql_url = URL.create(
        drivername,
        username,
        password,
        host,
        port,
        database
    )
    engine = create_engine(sql_url)
    return engine

