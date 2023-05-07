from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, ObjectIdField


class RoleCreate(BaseModel):
    actor_type: str
    actor_id: str
    role_name: str
    resource: str


class Role(RoleCreate):
    id: ObjectIdField = None

    class Config:
        json_encoders = {ObjectId: str}


class RoleRepository(AbstractRepository[Role]):
    class Meta:
        collection_name = 'roles'
