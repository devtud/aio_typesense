from unittest import mock

from aio_typesense.types import CollectionDict
from tests.utils import DockerTestCase

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


class TestCollections(DockerTestCase):
    async def test_collections_get_no_collections(self):
        collections = await self.client.collections.retrieve()
        self.assertEqual(0, len(collections))

    async def test_collections_create(self):
        global collection_schema
        expected_response: CollectionDict = {**collection_schema}  # noqa
        expected_fields = []
        for field in expected_response["fields"]:
            expected_fields.append(
                {
                    "name": field["name"],
                    "type": field["type"],
                    "optional": field["optional"] if "optional" in field else False,
                    "facet": field["facet"] if "facet" in field else False,
                }
            )
        expected_response["fields"] = expected_fields
        expected_response["created_at"] = mock.ANY  # noqa
        expected_response["num_memory_shards"] = mock.ANY  # noqa

        created_col = await self.client.collections.create(collection_schema)

        self.assertEqual(expected_response, created_col)

    async def test_collections_get(self):
        created_col = await self.client.collections.create(collection_schema)
        self.assertIn("name", created_col)
        self.assertIn("fields", created_col)

        _ = await self.client.collections.create(
            {**collection_schema, "name": "fruits2"}  # noqa
        )
        _ = await self.client.collections.create(
            {**collection_schema, "name": "fruits3"}  # noqa
        )

        collections = await self.client.collections.retrieve()

        self.assertEqual(3, len(collections))
