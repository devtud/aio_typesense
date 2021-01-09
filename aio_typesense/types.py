from typing import Optional, List, Union, TypeVar, overload, Dict

try:
    from typing import TypedDict, Literal, Protocol
except ImportError as e:
    from typing_extensions import TypedDict, Literal, Protocol

T = TypeVar("T")


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


class SearchResponseFacetCountItem(TypedDict):
    counts: List[dict]
    field_name: str
    stats: List


class SearchResponse(Protocol[T]):
    @overload
    def __getitem__(
        self, item: Literal["facet_counts"]
    ) -> List[SearchResponseFacetCountItem]:
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
