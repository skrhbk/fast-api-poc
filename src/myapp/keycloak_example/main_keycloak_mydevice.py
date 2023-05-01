"""
Device Code, streaming output and wait for user authorization on browser
"""

import asyncio
import logging
import pathlib
import time
from configparser import ConfigParser
from datetime import datetime, timedelta
from typing import Union

import requests
from authlib.integrations.requests_client import OAuth2Session
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer, HTTPBearer, \
    HTTPAuthorizationCredentials
from jose import JWTError, jwt
import json

from keycloak import KeycloakOpenID, KeycloakPostError
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.responses import StreamingResponse
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

# oauth2 = OAuth2PasswordBearer(
#     tokenUrl="token",
# )
get_bearer_token = HTTPBearer(auto_error=True)

app = FastAPI(
    # swagger_ui_oauth2_redirect_url= "/docs/oauth2-redirect"
    # swagger_ui_oauth2_redirect_url=kc_pub.auth_url("http://localhost:8000/doc/")
    swagger_ui_init_oauth={"clientId": conf['keycloak-public']['CLIENT_ID']}
)


def wait_device_auth(kc, device_code, verify_url):
    while True:
        try:
            token = kc.token(device_code=device_code,
                             grant_type="urn:ietf:params:oauth:grant-type:device_code")
            yield json.dumps(token)
            logger.info(f"Device[{device_code}] authenticated")
            break
        except KeycloakPostError as e:
            msg = f"Waiting for user verification vai URL[{verify_url}]"
            status = {"status": "Pending", "message": msg}
            logger.info(status)
            yield json.dumps(status)
        # await asyncio.sleep(5)
        time.sleep(5)


@app.post("/token")
async def login_keycloak():
    url = kc.well_known()['device_authorization_endpoint']
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(url=url, headers=headers,
                         data={"client_id": conf['keycloak']['CLIENT_ID'],
                               "client_secret": conf['keycloak']['SECRET_KEY']})

    device_auth = json.loads(resp.content.decode())
    logger.info(f"Please verify via URL: {device_auth['verification_uri_complete']}")
    # token = wait_device_auth(kc, device_auth['device_code'])
    # # return token

    return StreamingResponse(wait_device_auth(kc, device_auth['device_code'], device_auth['verification_uri_complete']),
                             media_type='application/x-ndjson')


@app.post("/token/refresh")
async def refresh_keycloak(auth: Annotated[HTTPAuthorizationCredentials, Depends(get_bearer_token)]):
    token = kc.refresh_token(auth.credentials)
    return token


@app.post("/token/logout")
async def logout_keycloak(auth: Annotated[HTTPAuthorizationCredentials, Depends(get_bearer_token)]):
    token = kc.logout(auth.credentials)
    return {"status": "Succeeded", "message": "Refresh token revoked."}


async def authenticate_bearer(auth: Annotated[HTTPAuthorizationCredentials, Depends(get_bearer_token)]):
    # Simulate a database query to find a known token
    # logger.info(f"auth.credentials[{auth.credentials}]")
    return auth.credentials


async def get_current_active_user(token: Annotated[str, Depends(authenticate_bearer)]):
    userinfo = kc.introspect(token)
    logger.info(f"userinfo={pretty_json(userinfo)}")
    if not userinfo["active"]:
        raise HTTPException(status_code=400, detail="Inactive user")

    user = User(username=userinfo['preferred_username'], email=userinfo['email'], full_name=userinfo['name'])
    return user


# async def get_current_active_user(access_token: Annotated[str, Depends(oauth2)]):
#     userinfo = kc.userinfo(access_token)
#     logger.debug(f"userinfo={pretty_json(userinfo)}")
#
#     user = User(username=userinfo['preferred_username'], email=userinfo['email'], full_name=userinfo['name'])
#     return user


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