from httpx import Response

from serp_onpremise.base import APIBase, APIBaseAsync, Base


class TokensBase(Base):
    def get_url(self, key: str = None) -> str:
        if key:
            return self.settings["base_url"] + f"/v1/tokens/access/{key}/"
        else:
            return self.settings["base_url"] + "/v1/tokens/access/"


class Impl(APIBase, TokensBase):
    def create(self, permanent: bool = False) -> Response:
        data = {"permanent": permanent}

        with self.get_client() as client:
            return client.post(url=self.get_url(), json=data)

    def list(
        self, permanent: bool = None, limit: int = 20, offset: int = 0
    ) -> Response:
        if permanent is not None:
            data = {"permanent": permanent, "limit": limit, "offset": offset}
        else:
            data = {"limit": limit, "offset": offset}

        with self.get_client() as client:
            return client.get(url=self.get_url(), params=data)

    def get(self, id: int) -> Response:
        with self.get_client() as client:
            return client.get(url=self.get_url(f"{id}"))

    def update(self, id: int, is_active: bool) -> Response:
        with self.get_client() as client:
            return client.patch(
                url=self.get_url(f"{id}"),
                data={"is_active": is_active},
            )

    def delete_list(self, permanent: bool = None) -> Response:
        data = {"permanent": permanent} if permanent is not None else None

        with self.get_client() as client:
            return client.delete(url=self.get_url(), params=data)

    def delete(self, id: int) -> Response:
        with self.get_client() as client:
            return client.delete(url=self.get_url(f"{id}"))


class ImplAsync(APIBaseAsync, TokensBase):
    async def create(self, permanent: bool = False) -> Response:
        data = {"permanent": permanent}

        async with self.get_client() as client:
            return await client.post(url=self.get_url(), json=data)

    async def list(
        self, permanent: bool = None, limit: int = 20, offset: int = 0
    ) -> Response:
        if permanent is not None:
            data = {"permanent": permanent, "limit": limit, "offset": offset}
        else:
            data = {"limit": limit, "offset": offset}

        async with self.get_client() as client:
            return await client.get(url=self.get_url(), params=data)

    async def get(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.get(url=self.get_url(f"{id}"))

    async def update(self, id: int, is_active: bool) -> Response:
        async with self.get_client() as client:
            return await client.patch(
                url=self.get_url(f"{id}"),
                data={"is_active": is_active},
            )

    async def delete_list(self, permanent: bool = None) -> Response:
        data = {"permanent": permanent} if permanent is not None else None

        async with self.get_client() as client:
            return await client.delete(url=self.get_url(), params=data)

    async def delete(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.delete(url=self.get_url(f"{id}"))
