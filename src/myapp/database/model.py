from typing import Union

from pydantic import AnyUrl, BaseModel, EmailStr, Field, constr
from pydantic import BaseModel
from pydantic_mongo import ObjectIdField
from bson import ObjectId


class User(BaseModel):
    id: ObjectIdField = None
    username: str
    hashed_password: Union[str, None] = None
    email: Union[EmailStr, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

    class Config:
        json_encoders = {ObjectId: str}


# class UserInDB(User):
#     hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str
