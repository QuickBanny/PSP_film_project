from sqlalchemy import create_engine

from db.config import DBConfig
from context import Context
from db.database import DataBase


def init_db(config: DBConfig, context: Context):
    engine = create_engine(
        config.url,
        pool_pre_ping=True,
    )
    database = DataBase(connection=engine)
    database.check_connection()

    context.set('database', database)