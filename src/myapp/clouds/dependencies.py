from typing import Annotated, Generator

from fastapi import Depends

from .service import CloudService
from ..database.dependencies import db_dep


async def get_cloud(db: db_dep) -> Generator:
    try:
        srv = CloudService(db)
        yield srv
    finally:
        pass


cloud_dep = Annotated[CloudService, Depends(get_cloud)]

