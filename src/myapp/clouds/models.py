from typing import List

from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, ObjectIdField


class CloudPatch(BaseModel):
    resources: List[str]


class CloudCreate(CloudPatch):
    cloud: str
    region: str


class Cloud(CloudCreate):
    id: ObjectIdField = None

    class Config:
        json_encoders = {ObjectId: str}


class CloudRepository(AbstractRepository[Cloud]):
    class Meta:
        collection_name = 'clouds'
