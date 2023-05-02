from datetime import timedelta
from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .models import Token
from .service import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..database.dependencies import db_dep

logger = getLogger("AuthRouter")

router = APIRouter(
    prefix="/token",
    tags=["token"],
    responses={404: {"description": "token not found"}}
)


@router.post("", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dep
):
    logger.info(f"login_for_access_token: {form_data.username}")
    user = authenticate_user(db.get_user(form_data.username), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
