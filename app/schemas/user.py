import datetime as _dt

import pydantic as _pydantic

class _UserBase(_pydantic.BaseModel):
    email: str
    # _pydantic.EmailStr

class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True

class User(_UserBase):
    id: int

    class Config:
        orm_mode = True
