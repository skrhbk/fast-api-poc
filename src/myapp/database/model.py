from typing import Union

from pydantic import BaseModel
from pydantic_mongo import ObjectIdField
from bson import ObjectId


class User(BaseModel):
    id: ObjectIdField = None
    username: str
    hashed_password: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

    class Config:
        json_encoders = {ObjectId: str}


# class UserInDB(User):
#     hashed_password: str
