from db.config import DBConfig
from transport.config import SanicConfig


class ApplicationConfig:
    sanic: SanicConfig
    database: DBConfig

    def __init__(self):
        self.sanic = SanicConfig()
        self.database = DBConfig()
