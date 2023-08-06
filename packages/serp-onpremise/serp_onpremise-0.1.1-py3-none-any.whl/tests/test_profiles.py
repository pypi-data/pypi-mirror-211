import os

import pytest
import respx

BASE_URL = "http://localhost:8080"


@respx.mock
def test_create_201(client):
    request = respx.post(f"{BASE_URL}/v1/profiles/").respond(
        status_code=201,
        json={"result": "new", "confidence": 100},
    )
    response = client.profiles.create(
        b"image", "test_source", 1000, True, True
    )

    assert request.called
    assert response.status_code == 201


@respx.mock
def test_create_201_buffer_reader(client):
    request = respx.post(f"{BASE_URL}/v1/profiles/").respond(
        status_code=201,
        json={"result": "new", "confidence": 100},
    )
    filename = "image.jpg"
    image_data = b"test_image_data"

    with open(filename, "wb") as f:
        f.write(image_data)

    with open(filename, "rb") as f:
        response = client.profiles.create(f, "test_source", 1000, True, True)

    os.remove(filename)

    assert request.called
    assert response.status_code == 201


@respx.mock
def test_create_201_tuple(client):
    request = respx.post(f"{BASE_URL}/v1/profiles/").respond(
        status_code=201,
        json={"result": "new", "confidence": 100},
    )
    filename = "image.jpg"
    image_data = b"test_image_data"

    with open(filename, "wb") as f:
        f.write(image_data)

    with open(filename, "rb") as f:
        response = client.profiles.create(
            (filename, f), "test_source", 1000, True, True
        )

    os.remove(filename)

    assert request.called
    assert response.status_code == 201


@respx.mock
def test_create_400(client):
    request = respx.post(f"{BASE_URL}/v1/profiles/").respond(status_code=400)
    response = client.profiles.create(
        b"image", "test_source", 1000, True, True, True
    )

    assert request.called
    assert response.status_code == 400


@respx.mock
@pytest.mark.asyncio
async def test_async_create_200(async_client):
    request = respx.post(f"{BASE_URL}/v1/profiles/").respond(
        status_code=201,
        json={"result": "new", "confidence": 100},
    )
    response = await async_client.profiles.create(
        b"image", "test_source", 1000, True, True
    )

    assert request.called
    assert response.status_code == 201


@respx.mock
@pytest.mark.asyncio
async def test_async_create_400(async_client):
    request = respx.post(f"{BASE_URL}/v1/profiles/").respond(status_code=400)
    response = await async_client.profiles.create(
        b"image", "test_source", 1000, True, True, True
    )

    assert request.called
    assert response.status_code == 400


@respx.mock
def test_delete(client):
    request = respx.delete(f"{BASE_URL}/v1/profiles/pid/").respond(
        status_code=204
    )
    response = client.profiles.delete("pid")

    assert request.called
    assert response.status_code == 204


@respx.mock
@pytest.mark.asyncio
async def test_async_delete(async_client):
    request = respx.delete(f"{BASE_URL}/v1/profiles/pid/").respond(
        status_code=204
    )
    response = await async_client.profiles.delete("pid")

    assert request.called
    assert response.status_code == 204


@respx.mock
def test_reinit_by_photo_204(client):
    request = respx.post(f"{BASE_URL}/v1/profiles/pid/reinit/").respond(
        status_code=204
    )
    response = client.profiles.reinit_by_photo(
        "pid", b"image", "source_name", 100
    )

    assert request.called
    assert response.status_code == 204


@respx.mock
def test_reinit_by_photo_400(client):
    request = respx.post(f"{BASE_URL}/v1/profiles/pid/reinit/").respond(
        status_code=400
    )
    response = client.profiles.reinit_by_photo(
        "pid", b"image", "source_name", 100, True
    )

    assert request.called
    assert response.status_code == 400


@respx.mock
@pytest.mark.asyncio
async def test_async_reinit_by_photo_204(async_client):
    request = respx.post(f"{BASE_URL}/v1/profiles/pid/reinit/").respond(
        status_code=204
    )
    response = await async_client.profiles.reinit_by_photo(
        "pid", b"image", "source_name", 100
    )

    assert request.called
    assert response.status_code == 204


@respx.mock
@pytest.mark.asyncio
async def test_async_reinit_by_photo_400(async_client):
    request = respx.post(f"{BASE_URL}/v1/profiles/pid/reinit/").respond(
        status_code=400
    )
    response = await async_client.profiles.reinit_by_photo(
        "pid", b"image", "source_name", 100, True
    )

    assert request.called
    assert response.status_code == 400


@respx.mock
def test_search_200(client):
    request = respx.post(f"{BASE_URL}/v1/profiles/search/").respond(
        status_code=200,
        json={"result": 2, "pid": "pid"},
    )
    response = client.profiles.search(b"photo")

    assert request.called
    assert response.status_code == 200
    assert response.json()["pid"] == "pid"


@respx.mock
def test_search_not_found_200(client):
    request = respx.post(f"{BASE_URL}/v1/profiles/search/").respond(
        status_code=200
    )
    response = client.profiles.search(b"photo")

    assert request.called
    assert response.status_code == 200


@respx.mock
@pytest.mark.asyncio
async def test_async_search_200(async_client):
    request = respx.post(f"{BASE_URL}/v1/profiles/search/").respond(
        status_code=200,
        json={"result": 2, "pid": "pid"},
    )
    response = await async_client.profiles.search(b"photo")

    assert request.called
    assert response.status_code == 200
    assert response.json()["pid"] == "pid"


@respx.mock
@pytest.mark.asyncio
async def test_async_not_found_200(async_client):
    request = respx.post(f"{BASE_URL}/v1/profiles/search/").respond(
        status_code=200
    )
    response = await async_client.profiles.search(b"image")

    assert request.called
    assert response.status_code == 200
