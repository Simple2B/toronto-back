import datetime as _dt
from enum import unique

import sqlalchemy as _sql
import sqlalchemy.orm as _orm
# import passlib as _hash
from passlib import hash

import app.database as _database

class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.hashed_password)
# $2b$12$VAtlxWYIf1SYrf3Z9Hw1xuPH0c/XCVcqmMOtWXa9/NhxuVW9./l6K
# $2b$12$VAtlxWYIf1SYrf3Z9Hw1xuPH0c/XCVcqmMOtWXa9/NhxuVW9./l6K