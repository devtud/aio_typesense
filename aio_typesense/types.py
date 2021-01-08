from typing import Optional, List, Union, TypeVar, overload, Dict

try:
    from typing import TypedDict, Literal, Protocol
except ImportError as e:
    from typing_extensions import TypedDict, Literal, Protocol

T = TypeVar("T", bound=TypedDict)


class SchemaFieldDict(TypedDict):
    name: str
    type: Union[Literal["string"], Literal["string[]"], Literal["int32"]]
    facet: Optional[bool]
    optional: Optional[bool]


class CollectionDict(TypedDict):
    name: str
    num_documents: int
    fields: List[SchemaFieldDict]
    default_sorting_field: str


class SearchResponseHit(Protocol[T]):
    @overload
    def __getitem__(self, item: Literal["highlights"]) -> List[Dict]:
        ...

    @overload
    def __getitem__(self, item: Literal["document"]) -> T:
        ...

    def __getitem__(self, item):
        return super().__getitem__(item)


class SearchResponse(Protocol[T]):
    @overload
    def __getitem__(self, item: Literal["facet_count"]) -> List:
        ...

    @overload
    def __getitem__(self, item: Literal["took_ms"]) -> int:
        ...

    @overload
    def __getitem__(self, item: Literal["found"]) -> int:
        ...

    @overload
    def __getitem__(self, item: Literal["hits"]) -> List[SearchResponseHit[T]]:
        ...

    def __getitem__(self, item):
        return super().__getitem__(item)


class SearchParams(TypedDict, total=False):
    q: Union[str, Literal["*"]]
    query_by: List[str]
    query_by_weights: Optional[List[int]]
    max_hits: Optional[Union[int, Literal["all"]]]
    prefix: Optional[bool]
    filter_by: Optional[str]
    sort_by: Optional[str]
    facet_by: Optional[str]
    max_facet_values: Optional[int]
    facet_query: Optional[str]
    num_typos: Optional[int]
    page: Optional[int]
    per_page: Optional[int]
    group_by: Optional[str]
    group_limit: Optional[int]
    include_fields: Optional[str]
    exclude_fields: Optional[str]
    highlight_full_fields: Optional[str]
    highlight_affix_num_tokens: Optional[int]
    highlight_start_tag: Optional[str]
    highlight_end_tag: Optional[str]
    snippet_threshold: Optional[int]
    drop_tokens_threshold: Optional[int]
    typo_tokens_threshold: Optional[int]
    pinned_hits: Optional[str]
    hidden_hits: Optional[str]
