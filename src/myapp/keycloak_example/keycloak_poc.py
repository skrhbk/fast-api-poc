import asyncio
import getpass

import requests
from keycloak import KeycloakOpenID, KeycloakPostError
from configparser import ConfigParser
import logging
import json
import time
logger = logging.getLogger()
logger.setLevel("INFO")
logging.basicConfig(level="INFO")

conf = ConfigParser()
conf.read("../app.ini")


def pretty_json(j) -> str:
    return json.dumps(j, indent=4, default=str, sort_keys=True)


async def wait_device_auth(kc, device_code):
    while True:
        try:
            return kc.token(device_code=device_code,
                            grant_type="urn:ietf:params:oauth:grant-type:device_code")
        except KeycloakPostError as e:
            logger.info(f"Waiting ...: {e}")
        await asyncio.sleep(5)

if __name__ == "__main__":
    # Configure client
    kc = KeycloakOpenID(server_url=conf['keycloak']['SERVER_URL'],
                        client_id=conf['keycloak']['CLIENT_ID'],
                        realm_name=conf['keycloak']['REALM_NAME'],
                        client_secret_key=conf['keycloak']['SECRET_KEY'])

    url = kc.well_known()['device_authorization_endpoint']
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(url=url, headers=headers,
                         data={"client_id": conf['keycloak']['CLIENT_ID'], "client_secret": conf['keycloak']['SECRET_KEY']})
    logger.info(f"code[{resp.status_code}], content[{resp.content}]")
    device_auth = json.loads(resp.content.decode())
    logger.info(device_auth['verification_uri_complete'])
    # device_code = getpass.getpass("Wait...")
    # token = kc.token(device_code=device_auth['device_code'], grant_type="urn:ietf:params:oauth:grant-type:device_code")
    token = asyncio.run(wait_device_auth(kc, device_auth['device_code']))
    logger.info(token)

def basic():
    # Configure client
    kc = KeycloakOpenID(server_url=conf['keycloak']['SERVER_URL'],
                        client_id=conf['keycloak']['CLIENT_ID'],
                        realm_name=conf['keycloak']['REALM_NAME'],
                        )
                        # client_secret_key="secret")

    # Get WellKnown
    logger.info(kc.well_known())

    token = kc.token("cckea", "079104")
    logger.info(f"expires_in[{token['expires_in']}], {pretty_json(token)}")

    access_token = token["access_token"]
    refresh_token = token["refresh_token"]

    userinfo = kc.userinfo(access_token)
    logger.info(userinfo)

    # kc.logout(refresh_token)

    # time.sleep(3)
    token_refreshed = kc.refresh_token(refresh_token)
    logger.info(f"expires_in[{token['expires_in']}], {pretty_json(token)}")

