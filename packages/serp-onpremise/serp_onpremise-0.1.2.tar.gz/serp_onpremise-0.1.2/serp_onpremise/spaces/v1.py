from typing import Optional

from httpx import Response

from serp_onpremise.base import APIBase, APIBaseAsync, Base
from serp_onpremise.utils import request_dict_processing


class SpacesBase(Base):
    def get_url(self, key: str = None) -> str:
        if key:
            return self.settings["base_url"] + f"/v1/spaces/{key}/"
        else:
            return self.settings["base_url"] + "/v1/spaces/"


class Impl(APIBase, SpacesBase):
    def create(
        self,
        name: str,
        ha_threshold: Optional[float] = None,
        junk_threshold: Optional[float] = None,
        search_threshold: Optional[float] = None,
        blur_min: Optional[float] = None,
        blur_max: Optional[float] = None,
        exp_min: Optional[float] = None,
        exp_max: Optional[float] = None,
        tilt_min: Optional[float] = None,
        tilt_max: Optional[float] = None,
        pan_min: Optional[float] = None,
        pan_max: Optional[float] = None,
        entry_storage_days: Optional[int] = None,
    ) -> Response:
        data = request_dict_processing(locals(), ["self"])

        with self.get_client() as client:
            return client.post(url=self.get_url(), json=data)

    def list(
        self, q: str = None, limit: int = 20, offset: int = 0
    ) -> Response:
        data = {"q": q, "limit": limit, "offset": offset}

        with self.get_client() as client:
            return client.get(url=self.get_url(), params=data)

    def get(self, id: int) -> Response:
        with self.get_client() as client:
            return client.get(url=self.get_url(f"{id}"))

    def update(
        self,
        id: int,
        name: Optional[str] = None,
        ha_threshold: Optional[float] = None,
        junk_threshold: Optional[float] = None,
        search_threshold: Optional[float] = None,
        blur_min: Optional[float] = None,
        blur_max: Optional[float] = None,
        exp_min: Optional[float] = None,
        exp_max: Optional[float] = None,
        tilt_min: Optional[float] = None,
        tilt_max: Optional[float] = None,
        pan_min: Optional[float] = None,
        pan_max: Optional[float] = None,
        entry_storage_days: Optional[int] = None,
    ) -> Response:
        data = request_dict_processing(locals(), ["id", "self"])

        with self.get_client() as client:
            return client.patch(url=self.get_url(f"{id}"), json=data)

    def delete(self, id: int) -> Response:
        with self.get_client() as client:
            return client.delete(url=self.get_url(f"{id}"))

    def token(self, id: int, permanent: bool = False) -> Response:
        data = {"permanent": permanent}

        with self.get_client() as client:
            return client.post(
                url=self.get_url(f"{id}/tokens/access"), json=data
            )


class ImplAsync(APIBaseAsync, SpacesBase):
    async def create(
        self,
        name: str,
        ha_threshold: Optional[float] = None,
        junk_threshold: Optional[float] = None,
        search_threshold: Optional[float] = None,
        blur_min: Optional[float] = None,
        blur_max: Optional[float] = None,
        exp_min: Optional[float] = None,
        exp_max: Optional[float] = None,
        tilt_min: Optional[float] = None,
        tilt_max: Optional[float] = None,
        pan_min: Optional[float] = None,
        pan_max: Optional[float] = None,
        entry_storage_days: Optional[int] = None,
    ) -> Response:
        data = request_dict_processing(locals(), ["self"])

        async with self.get_client() as client:
            return await client.post(url=self.get_url(), json=data)

    async def list(
        self, q: str = None, limit: int = 20, offset: int = 0
    ) -> Response:
        data = {"q": q, "limit": limit, "offset": offset}

        async with self.get_client() as client:
            return await client.get(url=self.get_url(), params=data)

    async def get(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.get(url=self.get_url(f"{id}"))

    async def update(
        self,
        id: int,
        name: Optional[str] = None,
        ha_threshold: Optional[float] = None,
        junk_threshold: Optional[float] = None,
        search_threshold: Optional[float] = None,
        blur_min: Optional[float] = None,
        blur_max: Optional[float] = None,
        exp_min: Optional[float] = None,
        exp_max: Optional[float] = None,
        tilt_min: Optional[float] = None,
        tilt_max: Optional[float] = None,
        pan_min: Optional[float] = None,
        pan_max: Optional[float] = None,
        entry_storage_days: Optional[int] = None,
    ) -> Response:
        data = request_dict_processing(locals(), ["id", "self"])

        async with self.get_client() as client:
            return await client.patch(url=self.get_url(f"{id}"), json=data)

    async def delete(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.delete(url=self.get_url(f"{id}"))

    async def token(self, id: int, permanent: bool = False) -> Response:
        data = {"permanent": permanent}

        async with self.get_client() as client:
            return await client.post(
                url=self.get_url(f"{id}/tokens/access"), json=data
            )
