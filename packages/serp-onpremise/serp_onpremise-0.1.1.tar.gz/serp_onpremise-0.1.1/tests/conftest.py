import asyncio

import pytest

from serp_onpremise import AsyncClient, Client


@pytest.fixture(scope="session")
def event_loop():
    """
    Run coroutines in non async code
    by using a new event_loop

    See: https://github.com/pytest-dev/pytest-asyncio/issues/93
    """
    old_loop = asyncio.get_event_loop()
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    try:
        yield new_loop
    finally:
        asyncio.set_event_loop(old_loop)


@pytest.fixture
def client_no_auth():
    return Client(base_url="http://localhost:8080")


@pytest.fixture
async def async_client_no_auth():
    return AsyncClient(base_url="http://localhost:8080")


@pytest.fixture
def client():
    return Client(api_token="token", base_url="http://localhost:8080")


@pytest.fixture
async def async_client():
    return AsyncClient(api_token="token", base_url="http://localhost:8080")
