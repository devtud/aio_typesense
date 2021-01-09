import json
from typing import List, Generic, TypeVar, Dict, Union

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

import httpx

from .api_call import ApiCall
from .types import SearchResponse

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

    async def delete(self) -> T:
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

    async def search(
        self,
        q: Union[str, Literal["*"]],
        query_by: Union[List[str], str],
        query_by_weights: Union[List[int], str] = None,
        max_hits: Union[int, Literal["all"]] = None,
        prefix: bool = None,
        filter_by: str = None,
        sort_by: str = None,
        facet_by: str = None,
        max_facet_values: int = None,
        facet_query: str = None,
        num_typos: int = None,
        page: int = None,
        per_page: int = None,
        group_by: str = None,
        group_limit: int = None,
        include_fields: str = None,
        exclude_fields: str = None,
        highlight_full_fields: str = None,
        highlight_affix_num_tokens: int = None,
        highlight_start_tag: str = None,
        highlight_end_tag: str = None,
        snippet_threshold: int = None,
        drop_tokens_threshold: int = None,
        typo_tokens_threshold: int = None,
        pinned_hits: str = None,
        hidden_hits: str = None,
    ) -> SearchResponse[T]:
        params = {
            "q": q,
            "query_by": ",".join(query_by) if isinstance(query_by, list) else query_by,
            "query_by_weights": (
                ",".join(query_by_weights)
                if isinstance(query_by_weights, list)
                else query_by_weights
            ),
            "max_hits": max_hits,
            "prefix": prefix,
            "filter_by": filter_by,
            "sort_by": sort_by,
            "facet_by": facet_by,
            "max_facet_values": max_facet_values,
            "facet_query": facet_query,
            "num_typos": num_typos,
            "page": page,
            "per_page": per_page,
            "group_by": group_by,
            "group_limit": group_limit,
            "include_fields": include_fields,
            "exclude_fields": exclude_fields,
            "highlight_full_fields": highlight_full_fields,
            "highlight_affix_num_tokens": highlight_affix_num_tokens,
            "highlight_start_tag": highlight_start_tag,
            "highlight_end_tag": highlight_end_tag,
            "snippet_threshold": snippet_threshold,
            "drop_tokens_threshold": drop_tokens_threshold,
            "typo_tokens_threshold": typo_tokens_threshold,
            "pinned_hits": pinned_hits,
            "hidden_hits": hidden_hits,
        }
        r = await self.api_call.request(
            method="GET",
            endpoint=self._endpoint_path("search"),
            params={k: v for k, v in params.items() if v is not None},
        )
        return json.loads(r)

    async def delete(self, params=None):
        r = await self.api_call.request(
            method="DELETE", endpoint=self._endpoint_path(), params=params
        )
        return json.loads(r)
