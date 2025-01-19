from sqlalchemy import create_engine
from sqlalchemy import URL, Connection, String, Integer

from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from src.constants import POSTGRESQL_HOST, POSTGRESQL_USER, POSTGRESQL_PASS, POSTGRESQL_PORT, POSTGRESQL_DB

drivername="postgresql+psycopg2"
host=POSTGRESQL_HOST
username=POSTGRESQL_USER
password=POSTGRESQL_PASS
port=POSTGRESQL_PORT
database=POSTGRESQL_DB

def get_engine() -> Connection:
    sql_url = URL.create(
        drivername,
        username,
        password,
        host,
        port,
        database
    )
    engine = create_engine(sql_url, echo=True)
    return engine


def create_db() -> tuple[Integer, String]:
    conn = get_engine()

    if not database_exists(conn.url):
        create_database(conn.url)
        return 200, "Database created successfully"
    else:
        return 200, "Database already exist"


def get_session(engine) -> String:
    Session = sessionmaker(engine)
    return Session()
