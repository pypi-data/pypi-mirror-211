from typing import Union

from httpx import Response

from serp_onpremise.base import APIBase, APIBaseAsync, Base
from serp_onpremise.constants import sentinel
from serp_onpremise.utils import request_query_processing


class UsersBase(Base):
    def get_url(self, key: str = None) -> str:
        if key:
            return self.settings["base_url"] + f"/v1/users/{key}/"
        else:
            return self.settings["base_url"] + "/v1/users/"


class Impl(APIBase, UsersBase):
    def list(
        self,
        q: Union[str, object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self"])
        with self.get_client() as client:
            return client.get(url=self.get_url(), params=data)

    def get(self, id: int) -> Response:
        with self.get_client() as client:
            return client.get(url=self.get_url(f"{id}"))

    def update(self, id: int, is_active: bool, username: str) -> Response:
        data = {"is_active": is_active, "username": username}
        with self.get_client() as client:
            return client.patch(url=self.get_url(f"{id}"), json=data)


class ImplAsync(APIBaseAsync, UsersBase):
    async def list(
        self,
        q: Union[str, object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self"])
        async with self.get_client() as client:
            return await client.get(url=self.get_url(), params=data)

    async def get(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.get(url=self.get_url(f"{id}"))

    async def update(
        self, id: int, is_active: bool, username: str
    ) -> Response:
        data = {"is_active": is_active, "username": username}
        async with self.get_client() as client:
            return await client.patch(url=self.get_url(f"{id}"), json=data)
