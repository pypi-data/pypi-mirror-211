import pytest
import respx

BASE_URL = "http://localhost:8080"

from tests.utils import mock_query_params_all_combos


@respx.mock
def test_create(client):
    request = respx.post(f"{BASE_URL}/v1/groups/profiles/").respond(
        status_code=201,
        json={"id": 1, "name": "test_name"},
    )
    response = client.groups_profiles.create("test_name")

    assert request.called
    assert response.status_code == 201
    assert response.json()["name"] == "test_name"


@respx.mock
@pytest.mark.asyncio
async def test_async_create(async_client):
    request = respx.post(f"{BASE_URL}/v1/groups/profiles/").respond(
        status_code=201,
        json={"id": 1, "name": "test_name"},
    )
    response = await async_client.groups_profiles.create("test_name")

    assert request.called
    assert response.status_code == 201
    assert response.json()["name"] == "test_name"


@respx.mock
def test_list_without_params_200(client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/groups/profiles", "limit=20", "offset=0"
    )
    response = client.groups_profiles.list()

    assert any([request.called for request in requests])
    assert response.status_code == 200


@respx.mock
def test_list_with_params_200(client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/groups/profiles",
        "limit=20",
        "offset=0",
        "person_ids_include=pid1,pid2".replace(",", "%2C"),
        "q=test",
    )
    response = client.groups_profiles.list(
        person_ids_include=["pid1", "pid2"], q="test"
    )

    assert any([request.called for request in requests])
    assert response.status_code == 200


@respx.mock
@pytest.mark.asyncio
async def test_async_list_without_params_200(async_client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/groups/profiles", "limit=20", "offset=0"
    )
    response = await async_client.groups_profiles.list()

    assert any([request.called for request in requests])
    assert response.status_code == 200


@respx.mock
@pytest.mark.asyncio
async def test_async_list_with_params_200(async_client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/groups/profiles",
        "limit=20",
        "offset=0",
        "person_ids_include=pid1,pid2".replace(",", "%2C"),
        "q=test",
    )
    response = await async_client.groups_profiles.list(
        person_ids_include=["pid1", "pid2"], q="test"
    )

    assert any([request.called for request in requests])
    assert response.status_code == 200


@respx.mock
def test_get_200(client):
    request = respx.get(f"{BASE_URL}/v1/groups/profiles/1/").respond(
        status_code=200,
        json={"id": 1, "name": "test"},
    )
    response = client.groups_profiles.get(1)

    assert request.called
    assert response.status_code == 200
    assert response.json()["id"] == 1


@respx.mock
@pytest.mark.asyncio
async def test_async_get_200(async_client):
    request = respx.get(f"{BASE_URL}/v1/groups/profiles/1/").respond(
        status_code=200,
        json={"id": 1, "name": "test"},
    )
    response = await async_client.groups_profiles.get(1)

    assert request.called
    assert response.status_code == 200
    assert response.json()["id"] == 1


@respx.mock
def test_update_200(client):
    request = respx.patch(f"{BASE_URL}/v1/groups/profiles/1/").respond(
        status_code=200,
        json={"id": 1, "name": "new_name"},
    )
    response = client.groups_profiles.update(1, name="new_name")

    assert request.called
    assert response.status_code == 200
    assert response.json()["name"] == "new_name"


@respx.mock
@pytest.mark.asyncio
async def test_async_update_200(async_client):
    request = respx.patch(f"{BASE_URL}/v1/groups/profiles/1/").respond(
        status_code=200,
        json={"id": 1, "name": "new_name"},
    )
    response = await async_client.groups_profiles.update(1, name="new_name")

    assert request.called
    assert response.status_code == 200
    assert response.json()["name"] == "new_name"


@respx.mock
def test_delete_204(client):
    request = respx.delete(f"{BASE_URL}/v1/groups/profiles/1/").respond(
        status_code=204
    )
    response = client.groups_profiles.delete(1)

    assert request.called
    assert response.status_code == 204


@respx.mock
@pytest.mark.asyncio
async def test_async_delete_204(async_client):
    request = respx.delete(f"{BASE_URL}/v1/groups/profiles/1/").respond(
        status_code=204
    )
    response = await async_client.groups_profiles.delete(1)

    assert request.called
    assert response.status_code == 204


@respx.mock
def test_persons_list_without_params_200(client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/groups/profiles/1/person_ids",
        "limit=20",
        "offset=0",
        json={
            "count": 1,
            "next": None,
            "prev": None,
            "data": [
                {
                    "person_id": "uuid",
                    "person_id_origin": "origin_name",
                    "profile_photo": "http://url/static/upload/image.png",
                }
            ],
        },
    )
    response = client.groups_profiles.person_ids(1)

    assert any([request.called for request in requests])
    assert response.status_code == 200
    assert response.json()["data"][0]["person_id"] == "uuid"


@respx.mock
def test_persons_list_with_params_200(client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/groups/profiles/1/person_ids",
        "limit=20",
        "offset=0",
        "person_ids=uuid,pid2".replace(",", "%2C"),
        json={
            "count": 1,
            "next": None,
            "prev": None,
            "data": [
                {
                    "person_id": "uuid",
                    "person_id_origin": "origin_name",
                    "profile_photo": "http://url/static/upload/image.png",
                }
            ],
        },
    )
    response = client.groups_profiles.person_ids(
        1, person_ids=["uuid", "pid2"]
    )

    assert any([request.called for request in requests])
    assert response.status_code == 200
    assert response.json()["data"][0]["person_id"] == "uuid"


@respx.mock
@pytest.mark.asyncio
async def test_async_persons_list_without_params_200(async_client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/groups/profiles/1/person_ids",
        "limit=20",
        "offset=0",
        json={
            "count": 1,
            "next": None,
            "prev": None,
            "data": [
                {
                    "person_id": "uuid",
                    "person_id_origin": "origin_name",
                    "profile_photo": "http://url/static/upload/image.png",
                }
            ],
        },
    )
    response = await async_client.groups_profiles.person_ids(1)

    assert any([request.called for request in requests])
    assert response.status_code == 200
    assert response.json()["data"][0]["person_id"] == "uuid"


@respx.mock
@pytest.mark.asyncio
async def test_async_persons_list_with_params_200(async_client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/groups/profiles/1/person_ids",
        "limit=20",
        "offset=0",
        "person_ids=uuid,pid2".replace(",", "%2C"),
        json={
            "count": 1,
            "next": None,
            "prev": None,
            "data": [
                {
                    "person_id": "uuid",
                    "person_id_origin": "origin_name",
                    "profile_photo": "http://url/static/upload/image.png",
                }
            ],
        },
    )
    response = await async_client.groups_profiles.person_ids(
        1, person_ids=["uuid", "pid2"]
    )

    assert any([request.called for request in requests])
    assert response.status_code == 200
    assert response.json()["data"][0]["person_id"] == "uuid"


@respx.mock
def test_add_persons_200(client):
    request = respx.post(f"{BASE_URL}/v1/groups/profiles/person_ids/").respond(
        status_code=200
    )
    response = client.groups_profiles.add_person_ids(
        person_ids=["pid"], groups_ids=[1, 2]
    )

    assert request.called
    assert response.status_code == 200


@respx.mock
@pytest.mark.asyncio
async def test_async_add_persons_200(async_client):
    request = respx.post(f"{BASE_URL}/v1/groups/profiles/person_ids/").respond(
        status_code=200
    )
    response = await async_client.groups_profiles.add_person_ids(
        person_ids=["pid"], groups_ids=[1, 2]
    )

    assert request.called
    assert response.status_code == 200


@respx.mock
def test_remove_persons_200(client):
    request = respx.delete(
        f"{BASE_URL}/v1/groups/profiles/person_ids/"
    ).respond(status_code=200)
    response = client.groups_profiles.remove_person_ids(
        person_ids=["pid"], groups_ids=[1, 2]
    )

    assert request.called
    assert response.status_code == 200


@respx.mock
@pytest.mark.asyncio
async def test_async_remove_persons_200(async_client):
    request = respx.delete(
        f"{BASE_URL}/v1/groups/profiles/person_ids/"
    ).respond(status_code=200)
    response = await async_client.groups_profiles.remove_person_ids(
        person_ids=["pid"], groups_ids=[1, 2]
    )

    assert request.called
    assert response.status_code == 200
