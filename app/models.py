import datetime as _dt
from enum import unique

import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib as _hash

import app.database as _database

class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)

    def varify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)
