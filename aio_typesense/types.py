from typing import (
    TypedDict,
    Optional,
    List,
    Literal,
    Union,
)


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
