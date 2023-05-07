from logging import getLogger
from typing import List, Annotated

from fastapi import APIRouter, Depends, Body

from .dependencies import rbac_dep, api_write_dep
from .models import Role, RoleCreate
from ..auth.dependencies import get_current_active_user

logger = getLogger("RoleRouter")

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "role not found"}}
)

query_example = {"actor_type": "type", "actor_id": "001", "role_name": "user", "resource": "gcp|us1|gpu"}


@router.get("", response_model=List[Role], response_model_exclude_unset=True)
async def list_roles(
        s: rbac_dep,
):
    """
    List all roles
    :return:
    """
    return s.list_roles({})


@router.post("/search", response_model=List[Role], response_model_exclude_unset=True)
async def list_roles(
        cond: Annotated[dict, Body(example=query_example)],
        s: rbac_dep,
):
    """
    List all roles
    :return:
    """
    return s.list_roles(cond)


@router.delete("", response_model_exclude_unset=True)
async def delete_role(
        cond: Annotated[dict, Body(example=query_example)],
        s: rbac_dep,
        _: api_write_dep
):
    """
    Delete one of the roles
    :return:
    """
    logger.info(f"delete role [{cond}]")
    return s.delete_role(cond)


@router.post("", response_model_exclude_unset=True)
async def create_role(
        role_create: RoleCreate,
        s: rbac_dep,
        _: api_write_dep
):
    """
    Create one role
    :return:
    """
    logger.info(f"create role [{role_create}]")
    return s.create_role(role_create)
