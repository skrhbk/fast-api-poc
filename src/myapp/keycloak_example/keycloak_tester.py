import asyncio
import json
import logging

import aiohttp
import requests
logger = logging.getLogger()
logger.setLevel("INFO")
logging.basicConfig(level="INFO")

# async def do_request():
#     proxy_url = 'http://localhost:8118'  # your proxy address
#     response = yield from aiohttp.request(
#         'GET', 'http://google.com',
#         proxy=proxy_url,
#     )
#     return response


def pretty_json(j) -> str:
    return json.dumps(j, indent=4, default=str, sort_keys=True)


async def do_post_request(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers) as resp:
            async for line in resp.content.iter_any():
                res = json.loads(line.decode())
                if "access_token" in res:
                    token = res
                else:
                    logger.info(res)
            # logger.debug(f"code[{resp.status}], content[{resp.content}]")
            # token = await resp.text()
            # logger.debug(f"token={token}")
            # aiohttp.StreamReader()
    return token

if __name__ == "__main__":
    # grant_type = device
    auth_url = "http://localhost:8000/token"
    headers = {"Content-Type": "application/x-ndjson"}
    token = asyncio.run(do_post_request(auth_url, headers))
    logger.info(pretty_json(token))

    # token = {
    #     "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJoMVJ3bXFPbUlPdHdGRXpzbXYwWkh1eHUxdjB5OXFYMkdlSUw4SXhFOFF3In0.eyJleHAiOjE2ODI4NTY1MzMsImlhdCI6MTY4Mjg1NjIzMywiYXV0aF90aW1lIjoxNjgyODUxMzAzLCJqdGkiOiJmNTBhNjQ2ZS1hMDAxLTRmZGItYmMyMC04NzMzOTc2MTBkOTMiLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwODAvcmVhbG1zL215cmVhbG0iLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiMzU4MWQ5NDktZWJlYS00N2I4LWJiNTItNjkwYWYyMDRkOGNhIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoibXljbGllbnQtY3JlZCIsInNlc3Npb25fc3RhdGUiOiJkNDMyYTY0YS1hODM1LTRmMWItOTI2ZC1lNjRjZjljMmM3ZGQiLCJhY3IiOiIwIiwiYWxsb3dlZC1vcmlnaW5zIjpbIi8qIiwiaHR0cDovL2xvY2FsaG9zdDo4MDAwIiwiaHR0cHM6Ly93d3cua2V5Y2xvYWsub3JnIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLW15cmVhbG0iLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwic2lkIjoiZDQzMmE2NGEtYTgzNS00ZjFiLTkyNmQtZTY0Y2Y5YzJjN2RkIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJDbGVtZW50IEtlIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiY2NrZWEiLCJnaXZlbl9uYW1lIjoiQ2xlbWVudCIsImZhbWlseV9uYW1lIjoiS2UiLCJlbWFpbCI6InNrcmhiaytteWtleWNsb2FrQGdtYWlsLmNvbSJ9.MzuE2bXMXCrKbWZPmyxtrVNOFBord3atMQoY3U5MXw1jwXUX3BA5_eylfyEvwKOQo2VTpEVKD7YAohIxuKysqsNFUmgLN4fEJCS3gq8SeYwba4ixkPBSItwcSMV_LRldyUPOnTTiumoEVdXzkGUhJnDwv0Uf7TODpQUqeYGazqanouX4DZQ7stMzS_iwWxOdZ6AgVv0Hl5BRfJva7XrMcx31PtiapXEg6XHG3QW8eCKma7yNMsDRG1rxvEOo1aid5mIDoalbTzuGaHz-q3WjXL2IFpi71cM_nvcjNHYIqh_vulO4EsTX2XiK84hUmTdf__ZYV_4wCCZNzxr4ZOKt9g",
    #     "expires_in": 300,
    #     "not-before-policy": 0,
    #     "refresh_expires_in": 1800,
    #     "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzOTZhZTYxYS02NzQ3LTQ4YmEtYTlhMi01NWVkZDExZDhlOTQifQ.eyJleHAiOjE2ODI4NTgwMzMsImlhdCI6MTY4Mjg1NjIzMywianRpIjoiMDgyMzljNWEtZmQ1OC00YWQ5LTkyZTUtMzE0MDEzOGU2ODUwIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9teXJlYWxtIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9teXJlYWxtIiwic3ViIjoiMzU4MWQ5NDktZWJlYS00N2I4LWJiNTItNjkwYWYyMDRkOGNhIiwidHlwIjoiUmVmcmVzaCIsImF6cCI6Im15Y2xpZW50LWNyZWQiLCJzZXNzaW9uX3N0YXRlIjoiZDQzMmE2NGEtYTgzNS00ZjFiLTkyNmQtZTY0Y2Y5YzJjN2RkIiwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwic2lkIjoiZDQzMmE2NGEtYTgzNS00ZjFiLTkyNmQtZTY0Y2Y5YzJjN2RkIn0.hZIv6TFCL0aKnF45bY32wrlEY2HumI4woimHtc3HcV0",
    #     "scope": "profile email",
    #     "session_state": "d432a64a-a835-4f1b-926d-e64cf9c2c7dd",
    #     "token_type": "Bearer"
    # }

    headers = {"Authorization": f"Bearer {token['access_token']}"}
    url = "http://localhost:8000/users/me"
    resp = requests.get(url, headers=headers)
    logger.info(f"code[{resp.status_code}], content[{resp.content}]")

    ot = token['access_token']

    if resp.status_code == 400:
    # if True:
        url = "http://localhost:8000/token/refresh"
        headers = {"Authorization": f"Bearer {token['refresh_token']}"}
        resp = requests.post(url, headers=headers)
        token = json.loads(resp.content.decode())
        logger.info(pretty_json(token))

    url = "http://localhost:8000/token/logout"
    headers = {"Authorization": f"Bearer {token['refresh_token']}"}
    resp = requests.post(url, headers=headers)
    logger.info(f"code[{resp.status_code}], content[{resp.content}]")

    # headers = {"Authorization": f"Bearer {ot}"}
    # url = "http://localhost:8000/users/me"
    # resp = requests.get(url, headers=headers)
    # logger.info(f"code[{resp.status_code}], content[{resp.content}]")

def password():
    # grant_type = password
    auth_url = "http://localhost:8000/token"
    # auth_url ="http://localhost:8080/realms/myrealm/protocol/openid-connect/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(url=auth_url, headers=headers,
                         data={"username": "cckea", "password": "079104"})
    logger.info(f"code[{resp.status_code}], content[{resp.content}]")
    token = json.loads(resp.content.decode())

    headers = {"Authorization": f"Bearer {token['access_token']}"}
    url = "http://localhost:8000/users/me"
    resp = requests.get(url, headers=headers)
    logger.info(f"code[{resp.status_code}], content[{resp.content}]")