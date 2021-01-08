import hashlib
import uuid

from db.models import BaseModel
from sqlalchemy import Column, VARCHAR, String


class DBUserModel(BaseModel):
    first_name = Column(VARCHAR(50))
    last_name = Column(VARCHAR(50))
    password = Column(String(120))
    email = Column(String(50))

    @staticmethod
    def hash_password(password):
        salt = uuid.uuid4.hex
        return hashlib.sha512(password + salt).hexdigest()

    def check_password(self, hash_password, password):
        if hash_password in self.hash_password(password):
            return True
        return False

