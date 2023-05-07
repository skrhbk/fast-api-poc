from logging import getLogger
from typing import List, Annotated

from .models import Cloud, CloudPatch, CloudCreate
from .service import CloudService
from fastapi import APIRouter, Depends

from ..auth.dependencies import get_current_active_user
from ..database.dependencies import get_db
from ..database.model import User
from ..database.mongo import MyMongo

logger = getLogger("CloudRouter")

router = APIRouter(
    prefix="/clouds",
    tags=["clouds"],
    responses={404: {"description": "cloud not found"}}
)


@router.get("", response_model=List[Cloud], response_model_exclude_unset=True)
async def list_clouds(
        db: Annotated[MyMongo, Depends(get_db)],
        _: Annotated[User, Depends(get_current_active_user)]):
    """
    List all clouds
    :return:
    """
    s = CloudService(db)
    return s.list_cloud()


@router.get("/{name}", response_model=List[Cloud], response_model_exclude_unset=True)
async def get_clouds(name: str,
                     db: Annotated[MyMongo, Depends(get_db)],
                     _: Annotated[User, Depends(get_current_active_user)]):
    """
    List all from one of the clouds
    :return:
    """
    logger.info(f"get_clouds [{name}]")
    s = CloudService(db)
    return s.get_cloud(name)


@router.patch("/{name}/{region}/{resource}", response_model_exclude_unset=True)
async def patch_cloud(name: str, region: str, resource: str,
                      cloud_patch: CloudPatch | None,
                      db: Annotated[MyMongo, Depends(get_db)],
                      _: Annotated[User, Depends(get_current_active_user)]):
    """
    Patch one of the clouds
    :return:
    """
    logger.info(f"patch cloud [{name}] + region[{region}] + resource[{resource}]")
    s = CloudService(db)
    return s.update_cloud(name, region, resource, cloud_patch)


@router.delete("/{name}/{region}/{resource}", response_model_exclude_unset=True)
async def delete_cloud(name: str, region: str, resource: str,
                       db: Annotated[MyMongo, Depends(get_db)],
                       _: Annotated[User, Depends(get_current_active_user)]):
    """
    Delete one of the clouds
    :return:
    """
    logger.info(f"delete cloud [{name}] + region[{region}] + resource[{resource}]")
    s = CloudService(db)
    return s.delete_cloud(name, region, resource)


@router.post("/{name}/{region}/{resource}", response_model_exclude_unset=True)
async def create_cloud(cloud_create: CloudCreate,
                       db: Annotated[MyMongo, Depends(get_db)],
                       _: Annotated[User, Depends(get_current_active_user)]):
    """
    Create one cloud
    :return:
    """
    logger.info(f"create cloud [{cloud_create}]")
    s = CloudService(db)
    return s.create_cloud(cloud_create)
