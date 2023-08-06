import abc

from httpx import AsyncClient, Client


class Base:
    def __init__(self, settings: dict) -> None:
        self.settings = settings


class APIBase(abc.ABC, Base):
    def get_client(self) -> Client:
        return Client(**self.settings)


class APIBaseAsync(abc.ABC, Base):
    def get_client(self) -> AsyncClient:
        return AsyncClient(**self.settings)
