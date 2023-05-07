from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends

from .dependencies import cloud_dep
from .models import Cloud, CloudPatch, CloudCreate
from ..auth.dependencies import get_current_active_user
from ..rbac.dependencies import api_write_dep

logger = getLogger("CloudRouter")

router = APIRouter(
    prefix="/clouds",
    tags=["clouds"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "cloud not found"}}
)


@router.get("", response_model=List[Cloud], response_model_exclude_unset=True)
async def list_clouds(
        s: cloud_dep,
):
    """
    List all clouds
    :return:
    """
    return s.list_cloud()


@router.get("/{name}", response_model=List[Cloud], response_model_exclude_unset=True)
async def get_clouds(
        name: str,
        s: cloud_dep,
):
    """
    List all from one of the clouds
    :return:
    """
    logger.info(f"get_clouds [{name}]")
    return s.get_cloud(name)


@router.patch("/{name}/{region}/{resource}", response_model_exclude_unset=True)
async def patch_cloud(
        name: str, region: str, resource: str,
        cloud_patch: CloudPatch | None,
        s: cloud_dep,
        _: api_write_dep
):
    """
    Patch one of the clouds
    :return:
    """
    logger.info(f"patch cloud [{name}] + region[{region}] + resource[{resource}]")
    return s.update_cloud(name, region, resource, cloud_patch)


@router.delete("/{name}/{region}/{resource}", response_model_exclude_unset=True)
async def delete_cloud(
        name: str, region: str, resource: str,
        s: cloud_dep,
        _: api_write_dep
):
    """
    Delete one of the clouds
    :return:
    """
    logger.info(f"delete cloud [{name}] + region[{region}] + resource[{resource}]")
    return s.delete_cloud(name, region, resource)


@router.post("", response_model_exclude_unset=True)
async def create_cloud(
        cloud_create: CloudCreate,
        s: cloud_dep,
        _: api_write_dep
):
    """
    Create one cloud
    :return:
    """
    logger.info(f"create cloud [{cloud_create}]")
    return s.create_cloud(cloud_create)
