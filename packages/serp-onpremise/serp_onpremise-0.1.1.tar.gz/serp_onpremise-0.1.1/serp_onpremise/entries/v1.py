from datetime import datetime
from typing import List, Union

from httpx import Response

from serp_onpremise.base import APIBase, APIBaseAsync, Base
from serp_onpremise.constants import sentinel
from serp_onpremise.utils import request_query_processing


class EntriesBase(Base):
    def get_url(self) -> str:
        return self.settings["base_url"] + "/v1/entries/"


class Impl(APIBase, EntriesBase):
    def list(
        self,
        person_ids: Union[List[str], object] = sentinel,
        conf: Union[List[int], object] = sentinel,
        age_from: Union[int, object] = sentinel,
        age_to: Union[int, object] = sentinel,
        sex: Union[int, object] = sentinel,
        mood: Union[List[str], object] = sentinel,
        origin_ids: Union[List[int], object] = sentinel,
        spaces_ids: Union[List[int], object] = sentinel,
        date_from: Union[datetime, object] = sentinel,
        date_to: Union[datetime, object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self"])
        with self.get_client() as client:
            return client.get(url=self.get_url(), params=data)


class ImplAsync(APIBaseAsync, EntriesBase):
    async def list(
        self,
        person_ids: Union[List[str], object] = sentinel,
        conf: Union[List[int], object] = sentinel,
        age_from: Union[int, object] = sentinel,
        age_to: Union[int, object] = sentinel,
        sex: Union[int, object] = sentinel,
        mood: Union[List[str], object] = sentinel,
        origin_ids: Union[List[int], object] = sentinel,
        spaces_ids: Union[List[int], object] = sentinel,
        date_from: Union[datetime, object] = sentinel,
        date_to: Union[datetime, object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self"])
        async with self.get_client() as client:
            return await client.get(url=self.get_url(), params=data)
