from typing import List

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

from aio_typesense.types import CollectionDict


def get_api_key():
    return "Rhsdhas2asasdasj2"


collection_schema: CollectionDict = {
    "name": "fruits",
    "num_documents": 0,
    "fields": [
        {
            "name": "name",
            "type": "string",
        },
        {
            "name": "timestamp",
            "type": "int32",
        },
        {
            "name": "description",
            "type": "string",
            "optional": True,
        },
        {
            "name": "color",
            "type": "string",
            "facet": True,
        },
    ],
    "default_sorting_field": "timestamp",
}


class AppleType(TypedDict):
    id: str
    timestamp: int
    name: str
    color: str


testing_documents: List[AppleType] = [
    {"id": "id1", "timestamp": 12341, "name": "Pink Pearl", "color": "pink"},
    {"id": "id2", "timestamp": 12342, "name": "Ambrosia", "color": "red"},
    {"id": "id3", "timestamp": 12343, "name": "Redlove Apples", "color": "red"},
    {"id": "id4", "timestamp": 12344, "name": "Macoun Apple", "color": "red"},
    {"id": "id5", "timestamp": 12345, "name": "Grimes Golden", "color": "yellow"},
    {"id": "id6", "timestamp": 12346, "name": "Opal", "color": "yellow"},
    {"id": "id7", "timestamp": 12347, "name": "Golden Delicious", "color": "yellow"},
]
