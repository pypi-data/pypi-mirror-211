from httpx import Response

from serp_onpremise.base import APIBase, APIBaseAsync, Base
from serp_onpremise.utils import FileType, prepare_file_processing


class ASMBase(Base):
    def get_url(self) -> str:
        return self.settings["base_url"] + "/v1/asm/"


class Impl(APIBase, ASMBase):
    def identify(self, image: FileType) -> Response:
        files = prepare_file_processing(image)
        with self.get_client() as client:
            return client.post(url=self.get_url(), files=files)


class ImplAsync(APIBaseAsync, ASMBase):
    async def identify(self, image: FileType) -> Response:
        files = prepare_file_processing(image)
        async with self.get_client() as client:
            return await client.post(url=self.get_url(), files=files)
