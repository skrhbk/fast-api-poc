# from fastapi import FastAPI
from fastapi.testclient import TestClient
from myapp.main import app


client = TestClient(app)


def test_read_main():
    response = client.get("token")
    assert response.status_code == 405
    print(str(response))
    # assert response.json() == {"msg": "Hello World"}