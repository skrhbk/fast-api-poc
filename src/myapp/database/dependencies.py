from typing import Annotated, Generator

from fastapi import Depends

from myapp.database.mongo import MyMongo


def get_db() -> Generator:
    try:
        db = MyMongo()
        yield db
    finally:
        db.close()


db_dep = Annotated[MyMongo, Depends(get_db)]
