from typing import Optional, List, Union, TypeVar, overload, Dict

try:
    from typing import TypedDict, Literal, Protocol
except ImportError:
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
        pass

    @overload
    def __getitem__(self, item: Literal["document"]) -> T:
        pass

    def __getitem__(self, item):
        pass


class SearchResponseFacetCountItem(TypedDict):
    counts: List[dict]
    field_name: str
    stats: List


class SearchResponse(Protocol[T]):
    @overload
    def __getitem__(
        self, item: Literal["facet_counts"]
    ) -> List[SearchResponseFacetCountItem]:
        pass

    @overload
    def __getitem__(self, item: Literal["took_ms"]) -> int:
        pass

    @overload
    def __getitem__(self, item: Literal["found"]) -> int:
        pass

    @overload
    def __getitem__(self, item: Literal["hits"]) -> List[SearchResponseHit[T]]:
        pass

    def __getitem__(self, item):
        pass
