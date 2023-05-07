from logging import getLogger

from pymongo.collection import Collection
from pymongo.results import InsertOneResult

from myapp.clouds.models import CloudRepository, Cloud, CloudPatch, CloudCreate
from myapp.database.mongo import MyMongo

logger = getLogger("CloudService")


class CloudService:
    def __init__(self, db: MyMongo):
        self._db = db.db
        self._coll: Collection = db.db.clouds

    def list_cloud(self):
        repo = CloudRepository(database=self._db)
        return list(repo.find_by({}))

    def get_cloud(self, name):
        repo = CloudRepository(database=self._db)
        return list(repo.find_by({"name": name}))

    def create_cloud(self, cloud_create: CloudCreate):
        repo = CloudRepository(database=self._db)
        result: InsertOneResult = repo.save(Cloud(**cloud_create.dict()))
        return result.acknowledged

    def update_cloud(self, name, region, resource, cloud_patch: CloudPatch):
        result = self._coll.update_one({"name": name, "region": region, "resource": resource}, {"$set": cloud_patch.dict()})
        return result.raw_result

    def delete_cloud(self, name, region, resource):
        result = self._coll.delete_one({"name": name, "region": region, "resource": resource})
        return result.raw_result

