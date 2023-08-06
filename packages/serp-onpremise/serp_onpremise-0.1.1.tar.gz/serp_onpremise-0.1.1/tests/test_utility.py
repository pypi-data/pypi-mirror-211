import pytest
import respx

BASE_URL = "http://localhost:8080"


@respx.mock
def test_test_compare_200(client):
    request = respx.post(f"{BASE_URL}/v1/compare/").respond(status_code=200)
    response = client.compare.identify(b"image1", b"image2")

    assert request.called
    assert response.status_code == 200


@respx.mock
@pytest.mark.asyncio
async def test_async_compare_200(async_client):
    request = respx.post(f"{BASE_URL}/v1/compare/").respond(status_code=200)
    response = await async_client.compare.identify(b"image1", b"image2")

    assert request.called
    assert response.status_code == 200


@respx.mock
def test_asm_200(client):
    request = respx.post(f"{BASE_URL}/v1/asm/").respond(status_code=200)
    response = client.asm.identify(b"image")

    assert request.called
    assert response.status_code == 200


@respx.mock
@pytest.mark.asyncio
async def test_async_asm_200(async_client):
    request = respx.post(f"{BASE_URL}/v1/asm/").respond(status_code=200)
    response = await async_client.asm.identify(b"image")

    assert request.called
    assert response.status_code == 200


@respx.mock
def test_test_liveness_200(client):
    request = respx.post(f"{BASE_URL}/v1/liveness/").respond(status_code=200)
    response = client.liveness.identify(b"image1", b"image2")

    assert request.called
    assert response.status_code == 200


@respx.mock
@pytest.mark.asyncio
async def test_async_liveness_200(async_client):
    request = respx.post(f"{BASE_URL}/v1/liveness/").respond(status_code=200)
    response = await async_client.liveness.identify(b"image1", b"image2")

    assert request.called
    assert response.status_code == 200
