from datetime import datetime

import pytest
import respx

BASE_URL = "http://localhost:8080"

from tests.utils import mock_query_params_all_combos


@respx.mock
def test_list_without_params200(client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/entries",
        "limit=20",
        "offset=0",
        json={
            "next": None,
            "prev": None,
            "data": [
                {
                    "id": 3373,
                    "space_id": 2,
                    "origin_id": 8,
                    "person_id": None,
                    "conf": 1,
                    "photo": "",
                    "created": "2021-09-29T15:01:45.392227+00:00",
                    "alive_probability": 0.9999799728393555,
                    "profile_photo": "",
                    "distance": None,
                    "exposure": 251369.71875,
                    "blur": 0.001,
                    "tilt": 18.51,
                    "pan": 8.53,
                    "age": 20,
                    "sex": 1,
                    "mood": "happy",
                }
            ],
        },
    )

    response = client.entries.list()
    assert any([request.called for request in requests])
    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == 3373


@respx.mock
def test_list_with_params200(client):
    date_str = "2018-06-29"
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/entries",
        "origin_ids=1,2,3".replace(",", "%2C"),
        f"date_from={date_str}",
        "limit=20",
        "offset=0",
        json={
            "next": None,
            "prev": None,
            "data": [
                {
                    "id": 3373,
                    "space_id": 2,
                    "origin_id": 8,
                    "person_id": None,
                    "conf": 1,
                    "photo": "",
                    "created": "2021-09-29T15:01:45.392227+00:00",
                    "alive_probability": 0.9999799728393555,
                    "profile_photo": "",
                    "distance": None,
                    "exposure": 251369.71875,
                    "blur": 0.001,
                    "tilt": 18.51,
                    "pan": 8.53,
                    "age": 20,
                    "sex": 1,
                    "mood": "happy",
                }
            ],
        },
    )

    response = client.entries.list(
        origin_ids=[1, 2, 3], date_from=date_obj.date()
    )

    assert any([request.called for request in requests])
    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == 3373


@respx.mock
@pytest.mark.asyncio
async def test_async_list_without_params_200(async_client):
    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/entries",
        "limit=20",
        "offset=0",
        json={
            "next": None,
            "prev": None,
            "data": [
                {
                    "id": 3373,
                    "space_id": 2,
                    "origin_id": 8,
                    "person_id": None,
                    "conf": 1,
                    "photo": "",
                    "created": "2021-09-29T15:01:45.392227+00:00",
                    "alive_probability": 0.9999799728393555,
                    "profile_photo": "",
                    "distance": None,
                    "exposure": 251369.71875,
                    "blur": 0.001,
                    "tilt": 18.51,
                    "pan": 8.53,
                    "age": 20,
                    "sex": 1,
                    "mood": "happy",
                }
            ],
        },
    )
    response = await async_client.entries.list()
    assert any([request.called for request in requests])
    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == 3373


@respx.mock
@pytest.mark.asyncio
async def test_async_list_with_params_200(async_client):
    date_str = "2018-06-29"
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    requests = mock_query_params_all_combos(
        f"{BASE_URL}/v1/entries",
        "origin_ids=1,2,3".replace(",", "%2C"),
        f"date_from={date_str}",
        "limit=20",
        "offset=0",
        json={
            "next": None,
            "prev": None,
            "data": [
                {
                    "id": 3373,
                    "space_id": 2,
                    "origin_id": 8,
                    "person_id": None,
                    "conf": 1,
                    "photo": "",
                    "created": "2021-09-29T15:01:45.392227+00:00",
                    "alive_probability": 0.9999799728393555,
                    "profile_photo": "",
                    "distance": None,
                    "exposure": 251369.71875,
                    "blur": 0.001,
                    "tilt": 18.51,
                    "pan": 8.53,
                    "age": 20,
                    "sex": 1,
                    "mood": "happy",
                }
            ],
        },
    )
    response = await async_client.entries.list(
        origin_ids=[1, 2, 3], date_from=date_obj.date()
    )
    assert any([request.called for request in requests])
    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == 3373
