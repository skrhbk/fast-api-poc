from typing import List

from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, ObjectIdField


class CloudPatch(BaseModel):
    gpu: int
    descr: str
    is_public: bool


class CloudCreate(CloudPatch):
    resource: str
    name: str
    region: str


class Cloud(CloudCreate):
    id: ObjectIdField = None

    @property
    def key(self):
        return f"{self.name}|{self.region}|{self.resource}"

    class Config:
        json_encoders = {ObjectId: str}


class CloudRepository(AbstractRepository[Cloud]):
    class Meta:
        collection_name = 'clouds'
