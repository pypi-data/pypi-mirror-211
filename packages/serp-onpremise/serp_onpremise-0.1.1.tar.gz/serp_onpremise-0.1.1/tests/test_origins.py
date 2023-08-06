import json

import pytest
import respx

BASE_URL = "http://localhost:8080"

from tests.utils import mock_query_params_all_combos


@respx.mock
def test_create_201(client):
    request = respx.post(f"{BASE_URL}/v1/origins/").respond(
        status_code=201,
        json={"id": 1, "name": "test_name"},
    )
    response = client.origins.create(name="test_name")

    request_content = request.calls[0][0]
    request_content.read()

    assert (
        "save_img_for_confs" not in json.loads(request_content.content).keys()
    )
    assert request.called
    assert response.status_code == 201
    assert response.json()["name"] == "test_name"


@respx.mock
def test_create_store_images_results_201(client):
    request = respx.post(f"{BASE_URL}/v1/origins/").respond(
        status_code=201,
        json={"id": 1, "name": "test_name"},
    )
    response = client.origins.create(
        name="test_name",
        save_img_for_confs=[6],
    )

    request_content = request.calls[0][0]
    request_content.read()

    assert "save_img_for_confs" in json.loads(request_content.content).keys()
    assert request.called
    assert response.status_code == 201
    assert response.json()["name"] == "test_name"


@respx.mock
@pytest.mark.asyncio
async def test_async_create_201(async_client):
    request = respx.post(f"{BASE_URL}/v1/origins/").respond(
        status_code=201,
        json={"id": 1, "name": "test_name"},
    )
    response = await async_client.origins.create(name="test_name")

    request_content = request.calls[0][0]
    request_content.read()

    assert (
        "save_img_for_confs" not in json.loads(request_content.content).keys()
    )
    assert request.called
    assert response.status_code == 201
    assert response.json()["name"] == "test_name"


@respx.mock
@pytest.mark.asyncio
async def test_async_create_store_images_results_201(async_client):
    request = respx.post(f"{BASE_URL}/v1/origins/").respond(
        status_code=201,
        json={"id": 1, "name": "test_name"},
    )
    response = await async_client.origins.create(
        name="test_name",
        save_img_for_confs=[6],
    )
    request_content = request.calls[0][0]
    request_content.read()

    assert "save_img_for_confs" in json.loads(request_content.content).keys()
    assert request.called
    assert response.status_code == 201
    assert response.json()["name"] == "test_name"


@respx.mock
def test_origins_list_without_params_200(client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/origins",
        "limit=20",
        "offset=0",
        "q=",
        json={"results": [{"id": 1, "name": "origin_name"}]},
    )
    response = client.origins.list()

    assert any([request.called for request in requests])
    assert response.status_code == 200
    assert response.json()["results"][0]["name"] == "origin_name"


@respx.mock
def test_origins_list_with_params_200(client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/origins",
        "q=test",
        "spaces_ids=1,2".replace(",", "%2C"),
        "limit=20",
        "offset=20",
        json={"results": [{"id": 1, "name": "origin_name"}]},
    )
    response = client.origins.list(q="test", offset=20, spaces_ids=[1, 2])

    assert any([request.called for request in requests])
    assert response.status_code == 200
    assert response.json()["results"][0]["name"] == "origin_name"


@respx.mock
@pytest.mark.asyncio
async def test_async_list_without_params_200(async_client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/origins",
        "limit=20",
        "offset=0",
        "q=",
        json={"results": [{"id": 1, "name": "origin_name"}]},
    )
    response = await async_client.origins.list()

    assert any([request.called for request in requests])
    assert response.status_code == 200
    assert response.json()["results"][0]["name"] == "origin_name"


@respx.mock
@pytest.mark.asyncio
async def test_async_list_with_params_200(async_client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/origins",
        "limit=20",
        "offset=20",
        "q=test",
        json={"results": [{"id": 1, "name": "origin_name"}]},
    )
    response = await async_client.origins.list(q="test", offset=20)

    assert any([request.called for request in requests])
    assert response.status_code == 200
    assert response.json()["results"][0]["name"] == "origin_name"


@respx.mock
def test_retrieve_200(client):
    request = respx.get(f"{BASE_URL}/v1/origins/1/").respond(
        status_code=200,
        json={"id": 1, "name": "origin_name"},
    )
    response = client.origins.get(id=1)
    assert request.called
    assert response.status_code == 200
    assert response.json()["name"] == "origin_name"


@respx.mock
def test_retrieve_404(client):
    request = respx.get(f"{BASE_URL}/v1/origins/1/").respond(status_code=404)
    response = client.origins.get(id=1)
    assert request.called
    assert response.status_code == 404


@respx.mock
@pytest.mark.asyncio
async def test_async_retrieve_200(async_client):
    request = respx.get(f"{BASE_URL}/v1/origins/1/").respond(
        status_code=200,
        json={"id": 1, "name": "origin_name"},
    )
    response = await async_client.origins.get(id=1)
    assert request.called
    assert response.status_code == 200
    assert response.json()["name"] == "origin_name"


@respx.mock
@pytest.mark.asyncio
async def test_async_retrieve_404(async_client):
    request = respx.get(f"{BASE_URL}/v1/origins/1/").respond(status_code=404)
    response = await async_client.origins.get(id=1)
    assert request.called
    assert response.status_code == 404


@respx.mock
def test_update_200(client):
    request = respx.patch(f"{BASE_URL}/v1/origins/1/").respond(
        status_code=200,
        json={"id": 1, "name": "origin_name"},
    )
    response = client.origins.update(id=1, name="origin_name")

    request_content = request.calls[0][0]
    request_content.read()

    assert request.called
    assert response.status_code == 200
    assert response.json()["name"] == "origin_name"


@respx.mock
@pytest.mark.asyncio
async def test_async_update_200(async_client):
    request = respx.patch(f"{BASE_URL}/v1/origins/1/").respond(
        status_code=200,
        json={"id": 1, "name": "origin_name"},
    )
    response = await async_client.origins.update(id=1, name="origin_name")

    request_content = request.calls[0][0]
    request_content.read()

    assert request.called
    assert response.status_code == 200
    assert response.json()["name"] == "origin_name"


@respx.mock
def test_delete_202(client):
    request = respx.delete(f"{BASE_URL}/v1/origins/1/").respond(
        status_code=202
    )
    response = client.origins.delete(id=1)
    assert request.called
    assert response.status_code == 202


@respx.mock
@pytest.mark.asyncio
async def test_async_delete_202(async_client):
    request = respx.delete(f"{BASE_URL}/v1/origins/1/").respond(
        status_code=202
    )
    response = await async_client.origins.delete(id=1)
    assert request.called
    assert response.status_code == 202
