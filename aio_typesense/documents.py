import json
from typing import List, Generic, TypeVar, Dict

import httpx

from .api_call import ApiCall
from .types import SearchParams, SearchResponse

T = TypeVar("T")


class _DocumentProxy(Generic[T]):
    def __init__(self, api_call: ApiCall, collection_name: str, document_id: str):
        self.api_call = api_call
        self.collection_name = collection_name
        self.document_id = document_id

    def _endpoint_path(self) -> str:
        return f"/collections/{self.collection_name}/documents/{self.document_id}"

    async def retrieve(self) -> T:
        try:
            r = await self.api_call.request(
                method="GET", endpoint=self._endpoint_path()
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == httpx.codes.NOT_FOUND:
                return None
            raise e
        return json.loads(r)

    async def update(self, document: T):
        r = await self.api_call.request(
            method="PATCH", endpoint=self._endpoint_path(), data=document
        )
        return json.loads(r)

    async def delete(self):
        r = await self.api_call.request(method="DELETE", endpoint=self._endpoint_path())
        return json.loads(r)


class Documents(Generic[T]):
    RESOURCE_PATH = "documents"

    def __init__(self, api_call: ApiCall, collection_name: str):
        self.api_call = api_call
        self.collection_name = collection_name
        self.documents: Dict[str, _DocumentProxy[T]] = {}

    def __getitem__(self, document_id) -> _DocumentProxy[T]:
        if document_id not in self.documents:
            self.documents[document_id] = _DocumentProxy(
                self.api_call, self.collection_name, document_id
            )

        return self.documents[document_id]

    def _endpoint_path(self, action: str = None) -> str:
        action = action or ""
        return f"/collections/{self.collection_name}/documents/{action}"

    async def create(self, document: T) -> T:
        r = await self.api_call.request(
            method="POST",
            endpoint=self._endpoint_path(),
            data=document,
            params={"action": "create"},
        )
        return json.loads(r)

    async def create_many(self, documents: List[T], params=None) -> List[dict]:
        return await self.import_(documents, params)

    async def upsert(self, document: T) -> T:
        r = await self.api_call.request(
            method="POST",
            endpoint=self._endpoint_path(),
            data=document,
            params={"action": "upsert"},
        )
        return json.loads(r)

    async def update(self, document: T) -> T:
        r = await self.api_call.request(
            method="POST",
            endpoint=self._endpoint_path(),
            data=document,
            params={"action": "update"},
        )
        return json.loads(r)

    async def import_(self, documents: List[T], params=None):

        content = "\n".join([json.dumps(d) for d in documents])

        api_response = await self.api_call.request(
            method="POST",
            endpoint=self._endpoint_path("import"),
            data=content.encode(),
            params=params,
        )

        res_obj_strs = api_response.split(b"\n")

        response_objs = []
        for res_obj_str in res_obj_strs:
            response_objs.append(json.loads(res_obj_str))

        return response_objs

    async def export(self):
        api_response = await self.api_call.request(
            method="GET",
            endpoint=self._endpoint_path("export"),
        )
        return api_response

    async def search(self, search_parameters: SearchParams) -> SearchResponse[T]:
        r = await self.api_call.request(
            method="GET",
            endpoint=self._endpoint_path("search"),
            params=search_parameters,
        )
        return json.loads(r)

    async def delete(self, params=None):
        r = await self.api_call.request(
            method="DELETE", endpoint=self._endpoint_path(), params=params
        )
        return json.loads(r)
