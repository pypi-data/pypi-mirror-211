from httpx import Response

from serp_onpremise.base import APIBase, APIBaseAsync, Base
from serp_onpremise.utils import FileType, prepare_file_processing


class LicensesBase(Base):
    def get_url(self) -> str:
        return self.settings["base_url"] + "/v1/licenses/"


class Impl(APIBase, LicensesBase):
    def set(self, license: FileType) -> Response:
        files = prepare_file_processing(license, key="license")
        with self.get_client() as client:
            return client.post(url=self.get_url(), files=files)

    def get(self) -> Response:
        with self.get_client() as client:
            return client.get(url=self.get_url())


class ImplAsync(APIBaseAsync, LicensesBase):
    async def set(self, license: FileType) -> Response:
        files = prepare_file_processing(license, key="license")
        async with self.get_client() as client:
            return await client.post(url=self.get_url(), files=files)

    async def get(self) -> Response:
        async with self.get_client() as client:
            return await client.get(url=self.get_url())
