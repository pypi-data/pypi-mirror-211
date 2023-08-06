from typing import List, Optional, Union

from httpx import Response

from serp_onpremise.base import APIBase, APIBaseAsync, Base
from serp_onpremise.constants import sentinel
from serp_onpremise.utils import (
    request_dict_processing,
    request_query_processing,
)


class OriginsBase(Base):
    def get_url(self, key: str = None) -> str:
        if key:
            return self.settings["base_url"] + f"/v1/origins/{key}/"
        else:
            return self.settings["base_url"] + "/v1/origins/"


class Impl(APIBase, OriginsBase):
    def create(
        self,
        name: str,
        min_facesize: int = 7000,
        save_img_for_confs: Union[Optional[List[int]], object] = sentinel,
        save_entries_for_confs: Union[Optional[List[int]], object] = sentinel,
        upload_create_ha: bool = False,
        upload_create_junk: bool = False,
        upload_create_min_facesize: int = 25000,
        upload_create_profile: bool = False,
        upload_filter_by_face_angle: bool = True,
        upload_create_filter_blur: bool = True,
        upload_create_filter_exp: bool = True,
        upload_identify_asm: bool = False,
        upload_identify_liveness: bool = False,
        create_min_facesize: int = 25000,
        create_ha: bool = False,
        create_junk: bool = False,
        create_identify_asm: bool = False,
        entry_storage_days: Optional[int] = None,
    ) -> Response:
        data = request_dict_processing(locals(), ["self"])

        with self.get_client() as client:
            return client.post(url=self.get_url(), json=data)

    def list(
        self,
        q: str = None,
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

    def update(
        self,
        id: int,
        name: str,
        min_facesize: int = 7000,
        save_img_for_confs: Union[Optional[List[int]], object] = sentinel,
        save_entries_for_confs: Union[Optional[List[int]], object] = sentinel,
        upload_create_ha: bool = False,
        upload_create_junk: bool = False,
        upload_create_min_facesize: int = 25000,
        upload_create_profile: bool = False,
        upload_filter_by_face_angle: bool = True,
        upload_create_filter_blur: bool = True,
        upload_create_filter_exp: bool = True,
        upload_identify_asm: bool = False,
        upload_identify_liveness: bool = False,
        create_min_facesize: int = 25000,
        create_ha: bool = False,
        create_junk: bool = False,
        create_identify_asm: bool = False,
        entry_storage_days: Optional[int] = None,
    ) -> Response:
        data = request_dict_processing(locals(), ["id", "self"])

        with self.get_client() as client:
            return client.patch(url=self.get_url(f"{id}"), json=data)

    def delete(self, id: int) -> Response:
        with self.get_client() as client:
            return client.delete(url=self.get_url(f"{id}"))


class ImplAsync(APIBaseAsync, OriginsBase):
    async def create(
        self,
        name: str,
        min_facesize: int = 7000,
        save_img_for_confs: Union[Optional[List[int]], object] = sentinel,
        save_entries_for_confs: Union[Optional[List[int]], object] = sentinel,
        upload_create_ha: bool = False,
        upload_create_junk: bool = False,
        upload_create_min_facesize: int = 25000,
        upload_create_profile: bool = False,
        upload_filter_by_face_angle: bool = True,
        upload_create_filter_blur: bool = True,
        upload_create_filter_exp: bool = True,
        upload_identify_asm: bool = False,
        upload_identify_liveness: bool = False,
        create_min_facesize: int = 25000,
        create_ha: bool = False,
        create_junk: bool = False,
        create_identify_asm: bool = False,
        entry_storage_days: Optional[int] = None,
    ) -> Response:
        data = request_dict_processing(locals(), ["self"])

        async with self.get_client() as client:
            return await client.post(url=self.get_url(), json=data)

    async def list(
        self,
        q: str = None,
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

    async def update(
        self,
        id: int,
        name: str,
        min_facesize: int = 7000,
        save_img_for_confs: Union[Optional[List[int]], object] = sentinel,
        save_entries_for_confs: Union[Optional[List[int]], object] = sentinel,
        upload_create_ha: bool = False,
        upload_create_junk: bool = False,
        upload_create_min_facesize: int = 25000,
        upload_create_profile: bool = False,
        upload_filter_by_face_angle: bool = True,
        upload_create_filter_blur: bool = True,
        upload_create_filter_exp: bool = True,
        upload_identify_asm: bool = False,
        upload_identify_liveness: bool = False,
        create_min_facesize: int = 25000,
        create_ha: bool = False,
        create_junk: bool = False,
        create_identify_asm: bool = False,
        entry_storage_days: Optional[int] = None,
    ) -> Response:
        data = request_dict_processing(locals(), ["id", "self"])

        async with self.get_client() as client:
            return await client.patch(url=self.get_url(f"{id}"), json=data)

    async def delete(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.delete(url=self.get_url(f"{id}"))
