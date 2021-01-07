import json
from typing import Union, List, Dict, Optional

import httpx

from aio_typesense.types import CollectionDict


class Documents(object):
    RESOURCE_PATH = "documents"

    def __init__(self, api_call: "ApiCall", collection_name: str):
        self.api_call = api_call
        self.collection_name = collection_name

    def _endpoint_path(self, action: str = None):

        action = action or ""
        return "{0}/{1}/{2}/{3}".format(
            Collections.RESOURCE_PATH,
            self.collection_name,
            Documents.RESOURCE_PATH,
            action,
        )

    async def create(self, document):
        return await self.api_call.request(
            method="POST",
            endpoint=self._endpoint_path(),
            data=document,
            params={"action": "create"},
        )

    async def create_many(self, documents: List[dict], params=None):
        return await self.import_(documents, params)

    async def upsert(self, document):
        return await self.api_call.request(
            method="POST",
            endpoint=self._endpoint_path(),
            data=document,
            params={"action": "upsert"},
        )

    async def update(self, document):
        return await self.api_call.request(
            method="POST",
            endpoint=self._endpoint_path(),
            data=document,
            params={"action": "update"},
        )

    # `documents` can be either a list of document objects (or)
    #  JSONL-formatted string containing multiple documents
    async def import_(self, documents: List[dict], params=None):

        api_response = await self.api_call.request(
            method="POST",
            endpoint=self._endpoint_path("import"),
            data=documents,
            params=params,
        )
        res_obj_strs = api_response.split(b"\n")

        response_objs = []
        for res_obj_str in res_obj_strs:
            response_objs.append(json.dumps(res_obj_str))

        return response_objs

    async def export(self):
        api_response = await self.api_call.request(
            method="GET",
            endpoint=self._endpoint_path("export"),
        )
        return api_response

    async def search(self, search_parameters):
        return await self.api_call.request(
            method="GET",
            endpoint=self._endpoint_path("search"),
            params=search_parameters,
        )

    async def delete(self, params=None):
        return await self.api_call.request(
            method="DELETE", endpoint=self._endpoint_path(), params=params
        )

    def delete_one(self, doc_id):
        ...


class Collection(object):
    def __init__(self, api_call: "ApiCall", name: str):
        self.name = name
        self.api_call = api_call
        self.documents = Documents(api_call, name)
        # self.overrides = Overrides(api_call, name)
        # self.synonyms = Synonyms(api_call, name)

    def _endpoint_path(self) -> str:
        return "{0}/{1}".format(Collections.RESOURCE_PATH, self.name)

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


class Collections:
    RESOURCE_PATH = "/collections"

    def __init__(self, api_call: "ApiCall"):
        self.api_call: ApiCall = api_call
        self.collections: Dict[str, Collection] = {}

    def __getitem__(self, collection_name: str) -> Collection:
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


class Client:
    def __init__(self, node_urls: List[str], api_key: str):
        self.collections: Collections = Collections(ApiCall(node_urls, api_key))


class ApiCall:
    def __init__(self, node_urls: List[str], api_key: str):
        self.node_urls = node_urls
        self.api_key = api_key

    async def request(
        self,
        *,
        method: str,
        endpoint: str,
        params: dict = None,
        data: Union[dict, list] = None,
    ) -> bytes:
        url = f"{self.node_urls[0]}/{endpoint.strip('/')}"
        headers = {
            "Content-Type": "application/json",
            "X-TYPESENSE-API-KEY": self.api_key,
        }

        async with httpx.AsyncClient() as http_client:
            r = await http_client.request(
                method=method, url=url, params=params, headers=headers, json=data
            )

        r.raise_for_status()

        return r.content
