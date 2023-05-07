from fastapi import Depends, FastAPI
from typing_extensions import Annotated

from .auth import router as auth_router
from .auth.dependencies import get_current_active_user
from .clouds import router as cloud_router
from .rbac import router as role_router
from .database.model import User

app = FastAPI(debug=True)

for r in [auth_router, cloud_router, role_router]:
    app.include_router(r.router, prefix="/v1")
    app.include_router(r.router, prefix="/latest")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]
