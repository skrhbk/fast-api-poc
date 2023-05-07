import pathlib
import urllib.parse
from configparser import ConfigParser

from pydantic_mongo import AbstractRepository
from pymongo import MongoClient
from pymongo.database import Database

from myapp import utils
from myapp.database.model import User
from myapp.log import getLogger

logger = getLogger("MongoClient")


class UserRepository(AbstractRepository[User]):
    class Meta:
        collection_name = 'users'


# class MyMongoContext:
#     def __init__(self):
#         self.db: MyMongo = MyMongo()
#
#     def __enter__(self):
#         logger.info("enter")
#         return self.db
#
#     def __exit__(self, exc_type, exc_value, traceback):
#         logger.info("exit")
#         self.db.close()


class MyMongo:
    def __init__(self):
        conf = ConfigParser()
        conf.read(utils.get_sibling_file_path(__file__, "app.ini"))

        host = "localhost"
        username = urllib.parse.quote_plus(conf['mongodb']['USER'])
        password = urllib.parse.quote_plus(conf['mongodb']['PASSWORD'])
        self.client: MongoClient= MongoClient(f"mongodb://{username}:{password}@{host}:{conf['mongodb']['PORT']}")
        self.db: Database = self.client.get_database(conf['mongodb']['DB'])
        logger.info(f"Get MongoDB client")

    def get_user(self, username):
        logger.debug(f"{username}")
        repo = UserRepository(database=self.db)
        return repo.find_one_by({"username": username})

    def close(self):
        self.client.close()


if __name__ == "__main__":
    mongo = MyMongo()
    # u = mongo.get_user("johndoe")
    # logger.info(u)
    # logger.info(u.username)

    # c = Cloud(name="gcp", region="us1", gpu=8, resource="a2", descr="Powerful GPU2")
    # repo.save(c)
    # c = Cloud(name="aws", region="jp", gpu=4, resource="a1", descr="Powerful GPU1")
    # repo.save(c)

    # from myapp.rbac.models import RoleRepository, Role
    # repo = RoleRepository(database=mongo.db)
    # data = {"actor_type": "project", "actor_id": "900001", "role_name": "user", "resource": "gcp|us1|a2"}
    # r = Role(**data)
    # repo.save(r)

    from myapp.clouds.models import CloudRepository, Cloud
    repo = CloudRepository(database=mongo.db)
    logger.info(repo.find_one_by({'name': "gcp"}))
    q = repo.get_pagination_query({}, after=0, before=10)
    logger.info(f"{q}: {list(repo.find_by(q))}")
    mongo.close()
