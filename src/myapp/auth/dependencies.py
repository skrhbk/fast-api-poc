from logging import getLogger
from typing import Annotated

from fastapi import Depends, HTTPException

from myapp.auth.service import get_current_user
from myapp.database.model import User

logger = getLogger("AuthDeps")


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    logger.info("get_current_active_user")
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
