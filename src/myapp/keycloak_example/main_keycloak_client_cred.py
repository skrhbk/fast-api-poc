"""
only for client (no resource owner or = user)
"""

import logging
import pathlib
from configparser import ConfigParser
from datetime import datetime, timedelta
from typing import Union

from authlib.integrations.requests_client import OAuth2Session
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.openapi.models import OAuthFlowClientCredentials, OAuthFlow
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer, OAuth2
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


app = FastAPI()


kc_pub = KeycloakOpenID(server_url=conf['keycloak-public']['SERVER_URL'],
                        client_id=conf['keycloak-public']['CLIENT_ID'],
                        realm_name=conf['keycloak-public']['REALM_NAME'],
                        )

kc = KeycloakOpenID(server_url=conf['keycloak']['SERVER_URL'],
                    client_id=conf['keycloak']['CLIENT_ID'],
                    realm_name=conf['keycloak']['REALM_NAME'],
                    client_secret_key=conf['keycloak']['SECRET_KEY']
                    )
# kc = KeycloakOpenID(server_url=conf['keycloak']['SERVER_URL'],
#                     client_id=conf['keycloak']['CLIENT_ID'],
#                     realm_name=conf['keycloak']['REALM_NAME'],
#                     )


logger.info(f"{kc.well_known()}")
logger.info(f"token_endpoint={kc.well_known()['token_endpoint']}")
oauth2 = OAuth2(
    flows=OAuthFlow(
        clientCredentials={
            "tokenUrl": kc_pub.well_known()['token_endpoint']
        }
    )
)


@app.post("/token", response_model=Token)
async def login_keycloak(access_token: Annotated[str, Depends(oauth2)]):
    return Token(token_type="bearer", access_token=access_token)


async def get_current_active_user(
    token: Annotated[Token, Depends(login_keycloak)]
):
    kc.decode_token()
    userinfo = kc.introspect(token.access_token)
    logger.debug(f"userinfo={pretty_json(userinfo)}")

    user = User(username= userinfo['preferred_username'], email=userinfo['email'], full_name=userinfo['name'])
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