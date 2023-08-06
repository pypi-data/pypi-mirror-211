import pytest
import respx
from httpx import Response

BASE_URL = "http://localhost:8080"


@respx.mock
def test_login_200(client_no_auth):
    request = respx.post(f"{BASE_URL}/v1/auth/token/").respond(
        status_code=200,
        json={"token": "key"},
    )
    login_response = client_no_auth.auth.token(
        username="helloworld", password="superpwd"
    )
    assert request.called
    assert login_response.status_code == 200
    assert login_response.json()["token"] == "key"


@respx.mock
@pytest.mark.asyncio
async def test_async_login_200(async_client_no_auth):
    request = respx.post(f"{BASE_URL}/v1/auth/token/").respond(
        status_code=200,
        json={"token": "key"},
    )
    login_response = await async_client_no_auth.auth.token(
        username="helloworld", password="superpwd"
    )
    assert request.called
    assert login_response.status_code == 200
    assert login_response.json()["token"] == "key"


@respx.mock
def test_password_change_200(client):
    request = respx.post(f"{BASE_URL}/v1/auth/password/change/").mock(
        return_value=Response(204)
    )
    response = client.auth.password_change(
        old_password="old_password", new_password="new_password"
    )
    assert request.called
    assert response.status_code == 204


@respx.mock
@pytest.mark.asyncio
async def test_async_password_change_200(async_client):
    request = respx.post(f"{BASE_URL}/v1/auth/password/change/").mock(
        return_value=Response(204)
    )
    response = await async_client.auth.password_change(
        old_password="old_password", new_password="new_password"
    )
    assert request.called
    assert response.status_code == 204
