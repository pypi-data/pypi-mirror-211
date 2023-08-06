import pytest
import respx

BASE_URL = "http://localhost:8080"


@respx.mock
def test_me_username_200(client):
    request = respx.get(f"{BASE_URL}/v1/whoami/").respond(
        status_code=200,
        json={"username": "name"},
    )
    response = client.whoami.get()
    assert request.called
    assert response.status_code == 200
    assert response.json()["username"] == "name"


@respx.mock
@pytest.mark.asyncio
async def test_async_me_username_200(async_client):
    request = respx.get(f"{BASE_URL}/v1/whoami/").respond(
        status_code=200,
        json={"username": "name"},
    )
    response = await async_client.whoami.get()
    assert request.called
    assert response.status_code == 200
    assert response.json()["username"] == "name"
