import pytest
import respx

BASE_URL = "http://localhost:8080"

from tests.utils import mock_query_params_all_combos


@respx.mock
def test_create_ok(client):
    request = respx.post(f"{BASE_URL}/v1/tokens/access/").respond(
        status_code=201,
        json={"is_active": True},
    )
    response = client.tokens.access.create()

    assert request.called
    assert response.status_code == 201
    assert response.json()["is_active"] is True


@respx.mock
def test_create_failed(client):
    request = respx.post(f"{BASE_URL}/v1/tokens/access/").respond(
        status_code=400
    )
    response = client.tokens.access.create(permanent=True)

    assert request.called
    assert response.status_code == 400


@respx.mock
@pytest.mark.asyncio
async def test_async_create_ok(async_client):
    request = respx.post(f"{BASE_URL}/v1/tokens/access/").respond(
        status_code=201,
        json={"is_active": True},
    )
    response = await async_client.tokens.access.create(permanent=True)

    assert request.called
    assert response.status_code == 201
    assert response.json()["is_active"] is True


@respx.mock
@pytest.mark.asyncio
async def test_async_create_failed(async_client):
    request = respx.post(f"{BASE_URL}/v1/tokens/access/").respond(
        status_code=400
    )
    response = await async_client.tokens.access.create(permanent=True)

    assert request.called
    assert response.status_code == 400


@respx.mock
def test_list_200(client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/tokens/access",
        "limit=20",
        "offset=0",
        json=[{"token": "key"}, {"token": "key2"}],
    )

    tokens = client.tokens.access.list()
    assert any([request.called for request in requests])
    assert tokens.status_code == 200
    assert tokens.json()[0]["token"] == "key"
    assert tokens.json()[1]["token"] == "key2"


@respx.mock
def test_permanent_list_200(client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/tokens/access",
        "permanent=true",
        "limit=20",
        "offset=0",
        json=[{"token": "key"}],
    )
    tokens = client.tokens.access.list(permanent=True)

    assert any([request.called for request in requests])
    assert tokens.status_code == 200
    assert tokens.json()[0]["token"] == "key"


@respx.mock
def test_not_permanent_list_200(client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/tokens/access",
        "permanent=false",
        "limit=20",
        "offset=0",
        json=[{"token": "key"}],
    )
    tokens = client.tokens.access.list(permanent=False)
    assert any([request.called for request in requests])
    assert tokens.status_code == 200
    assert tokens.json()[0]["token"] == "key"


@respx.mock
@pytest.mark.asyncio
async def test_async_list_200(async_client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/tokens/access",
        "limit=20",
        "offset=0",
        json=[{"token": "key"}, {"token": "key2"}],
    )
    tokens = await async_client.tokens.access.list()

    assert any([request.called for request in requests])
    assert tokens.status_code == 200
    assert tokens.json()[0]["token"] == "key"


@respx.mock
@pytest.mark.asyncio
async def test_async_permanent_list_200(async_client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/tokens/access",
        "permanent=true",
        "limit=20",
        "offset=0",
        json=[{"token": "key"}],
    )
    tokens = await async_client.tokens.access.list(permanent=True)

    assert any([request.called for request in requests])
    assert tokens.status_code == 200
    assert tokens.json()[0]["token"] == "key"


@respx.mock
@pytest.mark.asyncio
async def test_async_not_permanent_list_200(async_client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/tokens/access",
        "permanent=false",
        "limit=20",
        "offset=0",
        json=[{"token": "key"}],
    )
    tokens = await async_client.tokens.access.list(permanent=False)

    assert any([request.called for request in requests])
    assert tokens.status_code == 200
    assert tokens.json()[0]["token"] == "key"


@respx.mock
def test_token_info_by_id_200(client):
    request = respx.get(f"{BASE_URL}/v1/tokens/access/1/").respond(
        status_code=200,
        json={"key": "token", "is_active": True},
    )
    tokens = client.tokens.access.get(id=1)
    assert request.called
    assert tokens.status_code == 200
    assert tokens.json()["key"] == "token"


@respx.mock
def test_token_info_by_key_200(client):
    request = respx.get(f"{BASE_URL}/v1/tokens/access/token/").respond(
        status_code=200,
        json={"key": "token", "is_active": True},
    )
    tokens = client.tokens.access.get(id="token")
    assert request.called
    assert tokens.status_code == 200
    assert tokens.json()["key"] == "token"


@respx.mock
@pytest.mark.asyncio
async def test_async_info_by_id_200(async_client):
    request = respx.get(f"{BASE_URL}/v1/tokens/access/1/").respond(
        status_code=200,
        json={"key": "token", "is_active": True},
    )
    tokens = await async_client.tokens.access.get(id=1)
    assert request.called
    assert tokens.status_code == 200
    assert tokens.json()["key"] == "token"


@respx.mock
@pytest.mark.asyncio
async def test_async_info_by_key_200(async_client):
    request = respx.get(f"{BASE_URL}/v1/tokens/access/token/").respond(
        status_code=200,
        json={"key": "token", "is_active": True},
    )
    tokens = await async_client.tokens.access.get(id="token")
    assert request.called
    assert tokens.status_code == 200
    assert tokens.json()["key"] == "token"


@respx.mock
def test_token_update_by_key_200(client):
    request = respx.patch(f"{BASE_URL}/v1/tokens/access/token/").respond(
        status_code=200,
        json={"key": "token", "is_active": True},
    )
    tokens = client.tokens.access.update(id="token", is_active=True)
    assert request.called
    assert tokens.status_code == 200
    assert tokens.json()["key"] == "token"
    assert tokens.json()["is_active"]


@respx.mock
def test_token_update_by_id_deactivate_200(client):
    request = respx.patch(f"{BASE_URL}/v1/tokens/access/1/").respond(
        status_code=200,
        json={"key": "token", "is_active": False},
    )
    tokens = client.tokens.access.update(id=1, is_active=False)
    assert request.called
    assert tokens.status_code == 200
    assert tokens.json()["key"] == "token"
    assert tokens.json()["is_active"] is False


@respx.mock
@pytest.mark.asyncio
async def test_async_update_by_key_200(async_client):
    request = respx.patch(f"{BASE_URL}/v1/tokens/access/token/").respond(
        status_code=200,
        json={"key": "token", "is_active": True},
    )
    tokens = await async_client.tokens.access.update(
        id="token", is_active=True
    )
    assert request.called
    assert tokens.status_code == 200
    assert tokens.json()["key"] == "token"
    assert tokens.json()["is_active"]


@respx.mock
@pytest.mark.asyncio
async def test_async_update_by_id_deactivate_200(async_client):
    request = respx.patch(f"{BASE_URL}/v1/tokens/access/1/").respond(
        status_code=200,
        json={"key": "token", "is_active": False},
    )
    tokens = await async_client.tokens.access.update(id=1, is_active=False)
    assert request.called
    assert tokens.status_code == 200
    assert tokens.json()["key"] == "token"
    assert tokens.json()["is_active"] is False


@respx.mock
def test_delete(client):
    request = respx.delete(f"{BASE_URL}/v1/tokens/access/").respond(
        status_code=204
    )
    response = client.tokens.access.delete_list()
    assert request.called
    assert response.status_code == 204


@respx.mock
def test_delete_permanent(client):
    request = respx.delete(
        f"{BASE_URL}/v1/tokens/access/?permanent=true"
    ).respond(status_code=204)
    response = client.tokens.access.delete_list(permanent=True)
    assert request.called
    assert response.status_code == 204


@respx.mock
@pytest.mark.asyncio
async def test_asyncs_delete(async_client):
    request = respx.delete(f"{BASE_URL}/v1/tokens/access/").respond(
        status_code=204
    )
    response = await async_client.tokens.access.delete_list()
    assert request.called
    assert response.status_code == 204


@respx.mock
@pytest.mark.asyncio
async def test_asyncs_delete_permanent(async_client):
    request = respx.delete(
        f"{BASE_URL}/v1/tokens/access/?permanent=true"
    ).respond(status_code=204)
    response = await async_client.tokens.access.delete_list(permanent=True)
    assert request.called
    assert response.status_code == 204


@respx.mock
def test_token_delete_by_key_204(client):
    request = respx.delete(f"{BASE_URL}/v1/tokens/access/token/").respond(
        status_code=204
    )
    response = client.tokens.access.delete(id="token")
    assert request.called
    assert response.status_code == 204


@respx.mock
def test_token_delete_by_id_204(client):
    request = respx.delete(f"{BASE_URL}/v1/tokens/access/1/").respond(
        status_code=204
    )
    response = client.tokens.access.delete(id=1)
    assert request.called
    assert response.status_code == 204


@respx.mock
@pytest.mark.asyncio
async def test_async_delete_by_key(async_client):
    request = respx.delete(f"{BASE_URL}/v1/tokens/access/token/").respond(
        status_code=204
    )
    response = await async_client.tokens.access.delete(id="token")
    assert request.called
    assert response.status_code == 204


@respx.mock
@pytest.mark.asyncio
async def test_async_delete_by_id(async_client):
    request = respx.delete(f"{BASE_URL}/v1/tokens/access/1/").respond(
        status_code=204
    )
    response = await async_client.tokens.access.delete(id=1)
    assert request.called
    assert response.status_code == 204
