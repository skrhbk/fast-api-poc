from logging import getLogger
from typing import Annotated

from fastapi import Depends, HTTPException, Request

from myapp.auth.service import get_current_user
from myapp.database.model import User

logger = getLogger("AuthDeps")


async def get_current_active_user(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)]
):
    logger.info("get_current_active_user")
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    request.state.current_user = current_user
    return current_user
