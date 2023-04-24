import pymongo
import urllib.parse
from pydantic_mongo import AbstractRepository
from pymongo.database import Database
from .model import User


class UserRepository(AbstractRepository[User]):
    class Meta:
        collection_name = 'users'


class MyMongoContext:
    def __init__(self):
        self.db: MyMongo = MyMongo()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


class MyMongo:
    def __init__(self):
        host = "localhost"
        username = urllib.parse.quote_plus('fastapi')
        password = urllib.parse.quote_plus('fastapi')
        self.client = pymongo.MongoClient(f"mongodb://{username}:{password}@{host}:27017")
        self.db: Database = self.client.get_database("fastapi")
        # db.list_collections()
        print(f"Authenticated: {username}")

    def get_user(self, username):
        repo = UserRepository(database=self.db)
        return repo.find_one_by({"username": username})

    def close(self):
        self.client.close()


if __name__ == "__main__":
    mongo = MyMongo()
    u = mongo.get_user("johndoe")
    print(u)
    print(u.username)
    mongo.close()
