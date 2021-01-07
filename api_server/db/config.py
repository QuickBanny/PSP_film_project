import os
from dotenv import load_dotenv

load_dotenv()


class DBConfig:
    name = os.getenv('dbname', 'db.sqlite')
    url = rf'sqlite:///{name}'
