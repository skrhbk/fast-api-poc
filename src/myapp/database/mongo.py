import pathlib
from configparser import ConfigParser
import pymongo
from pymongo import MongoClient
import urllib.parse
from pydantic_mongo import AbstractRepository
from pymongo.database import Database, Collection

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
        conf.read(f"{pathlib.Path(__file__).parent}/app.ini")

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

    from myapp.clouds.models import Cloud, CloudRepository
    repo = CloudRepository(database=mongo.db)
    # c = Cloud(cloud="gcp", region="us1", resources=["a1", "a2", "gpu"])
    c = Cloud(cloud="aws", region="jp", resources=["a1", "a2", "gpu"])
    repo.save(c)

    # logger.info(repo.find_one_by({'cloud': "gcp"}))
    q = repo.get_pagination_query({}, after=0, before=10)
    logger.info(f"{q}: {list(repo.find_by(q))}")
    mongo.close()
