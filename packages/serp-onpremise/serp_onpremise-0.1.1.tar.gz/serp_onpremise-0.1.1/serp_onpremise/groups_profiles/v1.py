from typing import List, Union

from httpx import Response

from serp_onpremise.base import APIBase, APIBaseAsync, Base
from serp_onpremise.constants import sentinel
from serp_onpremise.utils import request_query_processing


class GroupsBase(Base):
    def get_url(self, key: str = None) -> str:
        if key:
            return self.settings["base_url"] + f"/v1/groups/profiles/{key}/"
        else:
            return self.settings["base_url"] + "/v1/groups/profiles/"


class Impl(APIBase, GroupsBase):
    def create(self, name: str) -> Response:
        data = {"name": name}
        with self.get_client() as client:
            return client.post(url=self.get_url(), json=data)

    def list(
        self,
        q: Union[str, object] = sentinel,
        person_ids_include: Union[List[str], object] = sentinel,
        person_ids_exclude: Union[List[str], object] = sentinel,
        groups_ids: Union[List[int], object] = sentinel,
        spaces_ids: Union[List[int], object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self"])
        with self.get_client() as client:
            return client.get(url=self.get_url(), params=data)

    def get(self, id: int) -> Response:
        with self.get_client() as client:
            return client.get(url=self.get_url(f"{id}"))

    def update(self, id: int, name: str) -> Response:
        data = {"name": name}
        with self.get_client() as client:
            return client.patch(url=self.get_url(f"{id}"), json=data)

    def delete(self, id: int) -> Response:
        with self.get_client() as client:
            return client.delete(url=self.get_url(f"{id}"))

    def person_ids(
        self,
        id: int,
        person_ids: Union[List[str], object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self", "id"])

        with self.get_client() as client:
            return client.get(
                url=self.get_url(f"{id}/person_ids"), params=data
            )

    def add_person_ids(
        self, person_ids: List[str], groups_ids: List[int]
    ) -> Response:
        data = {"person_ids": person_ids, "groups_ids": groups_ids}
        with self.get_client() as client:
            return client.post(url=self.get_url("person_ids"), json=data)

    def remove_person_ids(
        self, person_ids: List[str], groups_ids: List[int]
    ) -> Response:
        data = {"person_ids": person_ids, "groups_ids": groups_ids}
        with self.get_client() as client:
            return client.request(
                "DELETE", url=self.get_url("person_ids"), json=data
            )


class ImplAsync(APIBaseAsync, GroupsBase):
    async def create(self, name: str) -> Response:
        data = {"name": name}
        async with self.get_client() as client:
            return await client.post(url=self.get_url(), json=data)

    async def list(
        self,
        q: Union[str, object] = sentinel,
        person_ids_include: Union[List[str], object] = sentinel,
        person_ids_exclude: Union[List[str], object] = sentinel,
        groups_ids: Union[List[int], object] = sentinel,
        spaces_ids: Union[List[int], object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self"])
        async with self.get_client() as client:
            return await client.get(url=self.get_url(), params=data)

    async def get(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.get(url=self.get_url(f"{id}"))

    async def update(self, id: int, name: str) -> Response:
        data = {"name": name}
        async with self.get_client() as client:
            return await client.patch(url=self.get_url(f"{id}"), json=data)

    async def delete(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.delete(url=self.get_url(f"{id}"))

    async def person_ids(
        self,
        id: int,
        person_ids: Union[List[str], object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self", "id"])

        async with self.get_client() as client:
            return await client.get(
                url=self.get_url(f"{id}/person_ids"), params=data
            )

    async def add_person_ids(
        self, person_ids: List[str], groups_ids: List[int]
    ) -> Response:
        data = {"person_ids": person_ids, "groups_ids": groups_ids}
        async with self.get_client() as client:
            return await client.post(url=self.get_url("person_ids"), json=data)

    async def remove_person_ids(
        self, person_ids: List[str], groups_ids: List[int]
    ) -> Response:
        data = {"person_ids": person_ids, "groups_ids": groups_ids}
        async with self.get_client() as client:
            return await client.request(
                "DELETE", url=self.get_url("person_ids"), json=data
            )
