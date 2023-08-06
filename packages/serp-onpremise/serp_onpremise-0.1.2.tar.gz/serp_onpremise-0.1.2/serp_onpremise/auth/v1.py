from httpx import Response

from serp_onpremise.base import APIBase, APIBaseAsync, Base


class AuthBase(Base):
    def get_url(self, key: str) -> str:
        return self.settings["base_url"] + f"/v1/auth/{key}/"


class Impl(APIBase, AuthBase):
    def token(self, username: str, password: str) -> Response:
        data = {"username": username, "password": password}

        with self.get_client() as client:
            return client.post(url=self.get_url("token"), data=data)

    def register(self, username: str, password: str) -> Response:
        data = {"username": username, "password": password}

        with self.get_client() as client:
            return client.post(url=self.get_url("register"), json=data)

    def password_change(
        self, old_password: str, new_password: str
    ) -> Response:
        data = {
            "old_password": old_password,
            "password": new_password,
            "password2": new_password,
        }

        with self.get_client() as client:
            return client.post(url=self.get_url("password/change"), json=data)


class ImplAsync(APIBaseAsync, AuthBase):
    async def token(self, username: str, password: str) -> Response:
        data = {"username": username, "password": password}

        async with self.get_client() as client:
            return await client.post(url=self.get_url("token"), data=data)

    async def register(self, username: str, password: str) -> Response:
        data = {"username": username, "password": password}

        async with self.get_client() as client:
            return await client.post(url=self.get_url("register"), json=data)

    async def password_change(
        self, old_password: str, new_password: str
    ) -> Response:
        data = {
            "old_password": old_password,
            "password": new_password,
            "password2": new_password,
        }

        async with self.get_client() as client:
            return await client.post(
                url=self.get_url("password/change"), json=data
            )
