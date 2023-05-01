"""
FastAPI + Keycloak endpoint directly
"""

import logging
import pathlib
from configparser import ConfigParser
from datetime import datetime, timedelta
from typing import Union

from authlib.integrations.requests_client import OAuth2Session
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
import json

from keycloak import KeycloakOpenID
from passlib.context import CryptContext
from pydantic import BaseModel
from typing_extensions import Annotated

logger = logging.getLogger()
logger.setLevel("INFO")
logging.basicConfig(level="INFO")

from myapp.database.model import User, Token
from myapp.database.mongo import MyMongo, MyMongoContext

conf = ConfigParser()
conf.read(f"{pathlib.Path(__file__).parent}/app.ini")


def pretty_json(j) -> str:
    return json.dumps(j, indent=4, default=str, sort_keys=True)


async def get_db():
    with MyMongoContext() as db:
        yield db
db_dep = Annotated[MyMongo, Depends(get_db)]


def get_kc_base_url():
    return f"{conf['keycloak']['SERVER_URL']}/auth/realms/{conf['keycloak']['REALM_NAME']}/protocol/openid-connect"

kc_pub = KeycloakOpenID(server_url=conf['keycloak-public']['SERVER_URL'],
                        client_id=conf['keycloak-public']['CLIENT_ID'],
                        realm_name=conf['keycloak-public']['REALM_NAME'],
                        )

kc = KeycloakOpenID(server_url=conf['keycloak']['SERVER_URL'],
                    client_id=conf['keycloak']['CLIENT_ID'],
                    realm_name=conf['keycloak']['REALM_NAME'],
                    client_secret_key=conf['keycloak']['SECRET_KEY']
                    )

oauth2 = OAuth2PasswordBearer(
    tokenUrl=kc_pub.well_known()['token_endpoint'],
)

print(kc_pub.auth_url("http://localhost:8000/doc/"))

app = FastAPI(
    # swagger_ui_oauth2_redirect_url= "/docs/oauth2-redirect"
    # swagger_ui_oauth2_redirect_url=kc_pub.auth_url("http://localhost:8000/doc/")
    # swagger_ui_init_oauth={"clientId": conf['keycloak-public']['CLIENT_ID']}
)


@app.post("/token", response_model=Token)
async def login_keycloak(access_token: Annotated[str, Depends(oauth2)]):
    return Token(token_type="bearer", access_token=access_token)


async def get_current_active_user(
    token: Annotated[Token, Depends(login_keycloak)]
):
    userinfo = kc.introspect(token.access_token)
    logger.debug(f"userinfo={pretty_json(userinfo)}")

    user = User(username=userinfo['preferred_username'], email=userinfo['email'], full_name=userinfo['name'])
    return user


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