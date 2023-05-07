from typing import Annotated, Generator

from fastapi import Depends, Request

from .service import RoleService
from ..database.dependencies import db_dep
from ..database.model import User


async def get_rbac(db: db_dep) -> Generator:
    try:
        rbac = RoleService(db)
        yield rbac
    finally:
        pass


rbac_dep = Annotated[RoleService, Depends(get_rbac)]


async def authorize_api_write(request: Request, rbac: rbac_dep):
    u: User = request.state.current_user
    return rbac.authorize("user", u.username, "write", request)

api_write_dep = Annotated[None, Depends(authorize_api_write)]
