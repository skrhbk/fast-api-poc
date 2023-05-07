import json
from logging import getLogger
from typing import List, Annotated

from .models import Role, RoleCreate
from .service import RoleService
from fastapi import APIRouter, Depends, Body

from ..auth.dependencies import get_current_active_user
from ..database.dependencies import get_db
from ..database.model import User
from ..database.mongo import MyMongo

logger = getLogger("RoleRouter")

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    responses={404: {"description": "role not found"}}
)

query_example = {"actor_type": "type", "actor_id": "001", "role_name": "user", "resource": "gcp|us1|gpu"}


@router.get("", response_model=List[Role], response_model_exclude_unset=True)
async def list_roles(
        db: Annotated[MyMongo, Depends(get_db)],
        _: Annotated[User, Depends(get_current_active_user)]):
    """
    List all roles
    :return:
    """
    s = RoleService(db)
    return s.list_roles({})


@router.post("/search", response_model=List[Role], response_model_exclude_unset=True)
async def list_roles(
        cond: Annotated[dict, Body(example=query_example)],
        db: Annotated[MyMongo, Depends(get_db)],
        _: Annotated[User, Depends(get_current_active_user)]):
    """
    List all roles
    :return:
    """
    s = RoleService(db)
    return s.list_roles(cond)


@router.delete("", response_model_exclude_unset=True)
async def delete_role(cond: Annotated[dict, Body(example=query_example)],
                      db: Annotated[MyMongo, Depends(get_db)],
                      _: Annotated[User, Depends(get_current_active_user)]):
    """
    Delete one of the roles
    :return:
    """
    logger.info(f"delete role [{cond}]")
    s = RoleService(db)
    return s.delete_role(cond)


@router.post("", response_model_exclude_unset=True)
async def create_role(role_create: RoleCreate,
                      db: Annotated[MyMongo, Depends(get_db)],
                      _: Annotated[User, Depends(get_current_active_user)]):
    """
    Create one role
    :return:
    """
    logger.info(f"create role [{role_create}]")
    s = RoleService(db)
    return s.create_role(role_create)
