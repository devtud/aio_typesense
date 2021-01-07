__all__ = [
    "get_api_key",
    "collection_schema",
]

from aio_typesense.types import CollectionDict


def get_api_key():
    return "Rhsdhas2asasdasj2"


collection_schema: CollectionDict = {
    "name": "fruits",
    "num_documents": 0,
    "fields": [
        {
            "name": "type",
            "type": "string",
            "facet": True,
        },
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
    ],
    "default_sorting_field": "timestamp",
}
