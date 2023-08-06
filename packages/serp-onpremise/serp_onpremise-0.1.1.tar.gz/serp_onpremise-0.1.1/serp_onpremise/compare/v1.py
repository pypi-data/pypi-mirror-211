from httpx import Response

from serp_onpremise.base import APIBase, APIBaseAsync, Base
from serp_onpremise.utils import FileType, prepare_file_processing


class CompareBase(Base):
    def get_url(self) -> str:
        return self.settings["base_url"] + "/v1/compare/"


class Impl(APIBase, CompareBase):
    def identify(self, image1: FileType, image2: FileType) -> Response:
        files1 = prepare_file_processing(image1, key="image1")
        files2 = prepare_file_processing(image2, key="image2")
        files1.update(files2)
        with self.get_client() as client:
            return client.post(url=self.get_url(), files=files1)


class ImplAsync(APIBaseAsync, CompareBase):
    async def identify(self, image1: FileType, image2: FileType) -> Response:
        files1 = prepare_file_processing(image1, key="image1")
        files2 = prepare_file_processing(image2, key="image2")
        files1.update(files2)
        async with self.get_client() as client:
            return await client.post(url=self.get_url(), files=files1)
