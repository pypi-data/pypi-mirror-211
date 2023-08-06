from typing import Optional, Union

from httpx import Response

from serp_onpremise.base import APIBase, APIBaseAsync, Base
from serp_onpremise.constants import EntryConf, sentinel
from serp_onpremise.utils import (
    FileType,
    prepare_file_processing,
    request_form_processing,
)


class ProfilesBase(Base):
    def get_url(self, key: str = None) -> str:
        if key:
            return self.settings["base_url"] + f"/v1/profiles/{key}/"
        else:
            return self.settings["base_url"] + "/v1/profiles/"


class Impl(APIBase, ProfilesBase):
    def create(
        self,
        image: FileType,
        origin_id: int,
        create_min_facesize: Union[int, object] = sentinel,
        create_ha: Union[bool, object] = sentinel,
        create_junk: Union[bool, object] = sentinel,
        identify_asm: Union[bool, object] = sentinel,
    ) -> Response:
        data = request_form_processing(locals(), ["self", "image"])
        files = prepare_file_processing(image)

        with self.get_client() as client:
            return client.post(url=self.get_url(), data=data, files=files)

    def delete(self, id: str) -> Response:
        with self.get_client() as client:
            return client.delete(url=self.get_url(f"{id}"))

    def reinit_by_photo(
        self,
        id: str,
        image: FileType,
        create_min_facesize: Union[int, object] = sentinel,
        min_conf: int = EntryConf.HA.value,
        identify_asm: Union[bool, object] = sentinel,
    ) -> Response:
        data = request_form_processing(locals(), ["self", "id", "image"])
        files = prepare_file_processing(image)

        with self.get_client() as client:
            return client.post(
                url=self.get_url(f"{id}/reinit"), data=data, files=files
            )

    def search(
        self,
        image: FileType,
        image2: Union[FileType, object] = sentinel,
        identify_asm: bool = False,
    ) -> Response:
        files = prepare_file_processing(image)
        if not isinstance(image2, object):
            files2 = prepare_file_processing(image2, key="image2")
            files.update(files2)
        data = {"identify_asm": str(identify_asm)}
        with self.get_client() as client:
            return client.post(
                url=self.get_url("search"), data=data, files=files
            )


class ImplAsync(APIBaseAsync, ProfilesBase):
    async def create(
        self,
        image: FileType,
        origin_id: int,
        create_min_facesize: Union[int, object] = sentinel,
        create_ha: Union[bool, object] = sentinel,
        create_junk: Union[bool, object] = sentinel,
        identify_asm: Union[bool, object] = sentinel,
    ) -> Response:
        data = request_form_processing(locals(), ["self", "image"])
        files = prepare_file_processing(image)

        async with self.get_client() as client:
            return await client.post(
                url=self.get_url(), data=data, files=files
            )

    async def delete(self, id: str) -> Response:
        async with self.get_client() as client:
            return await client.delete(url=self.get_url(f"{id}"))

    async def reinit_by_photo(
        self,
        id: str,
        image: FileType,
        create_min_facesize: Union[int, object] = sentinel,
        min_conf: int = EntryConf.HA.value,
        identify_asm: Union[bool, object] = sentinel,
    ) -> Response:
        data = request_form_processing(locals(), ["self", "id", "image"])
        files = prepare_file_processing(image)

        async with self.get_client() as client:
            return await client.post(
                url=self.get_url(f"{id}/reinit"), data=data, files=files
            )

    async def search(
        self,
        image: FileType,
        image2: Union[FileType, object] = sentinel,
        identify_asm: bool = False,
    ) -> Response:
        files = prepare_file_processing(image)
        if not isinstance(image2, object):
            files2 = prepare_file_processing(image2, key="image2")
            files.update(files2)
        data = {"identify_asm": str(identify_asm)}
        async with self.get_client() as client:
            return await client.post(
                url=self.get_url("search"), data=data, files=files
            )
