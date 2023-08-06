from httpx import Response

from serp_onpremise.base import APIBase, APIBaseAsync, Base


class WhoamiBase(Base):
    def get_url(self) -> str:
        return self.settings["base_url"] + "/v1/whoami/"


class Impl(APIBase, WhoamiBase):
    def get(self) -> Response:
        with self.get_client() as client:
            return client.get(url=self.get_url())


class ImplAsync(APIBaseAsync, WhoamiBase):
    async def get(self) -> Response:
        async with self.get_client() as client:
            return await client.get(url=self.get_url())
