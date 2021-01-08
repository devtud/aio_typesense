import json
from typing import Dict, Optional, Generic, TypeVar

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

import httpx

from .api_call import ApiCall
from .documents import Documents
from .types import CollectionDict

T = TypeVar("T")


class Collections:
    RESOURCE_PATH = "/collections"

    def __init__(self, api_call: ApiCall):
        self.api_call: ApiCall = api_call
        self.collections: Dict[str, Collection] = {}

    def __getitem__(self, collection_name: str) -> "Collection":
        if collection_name not in self.collections:
            self.collections[collection_name] = Collection(
                self.api_call, collection_name
            )

        return self.collections.get(collection_name)

    async def create(self, schema: CollectionDict) -> CollectionDict:
        r = await self.api_call.request(
            method="POST", endpoint=Collections.RESOURCE_PATH, data=schema
        )
        return json.loads(r)

    async def retrieve(self) -> CollectionDict:
        r = await self.api_call.request(
            method="GET", endpoint=Collections.RESOURCE_PATH
        )
        return json.loads(r)


class Collection(Generic[T]):
    def __init__(self, api_call: ApiCall, name: str):
        self.name = name
        self.api_call = api_call
        self.documents: Documents[T] = Documents(api_call, name)
        # self.overrides = Overrides(api_call, name)
        # self.synonyms = Synonyms(api_call, name)

    def _endpoint_path(self) -> str:
        return f"/collections/{self.name}"

    async def retrieve(self) -> Optional[CollectionDict]:
        try:
            r = await self.api_call.request(
                method="GET",
                endpoint=self._endpoint_path(),
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == httpx.codes.NOT_FOUND:
                return None
            raise e

        return json.loads(r)

    async def delete(self):
        r = await self.api_call.request(method="DELETE", endpoint=self._endpoint_path())
        return json.loads(r)
