import asyncio

from aio_typesense import Collection
from tests.common import collection_schema, testing_documents, AppleType
from tests.docker_ import DockerTestCase


class TestSearch(DockerTestCase):
    def setUp(self) -> None:
        super().setUp()
        loop = asyncio.get_event_loop()
        collection = loop.run_until_complete(
            self.client.collections.create(collection_schema)
        )
        self.assertEqual("fruits", collection["name"])

        result = loop.run_until_complete(
            self.client.collections["fruits"].documents.create_many(testing_documents)
        )
        for r in result:
            self.assertTrue(r["success"])

    async def test_search_general(self):
        collection: Collection[AppleType] = self.client.collections["fruits"]
        result = await collection.documents.search(q="apple", query_by=["name"])
        self.assertEqual(2, len(result["hits"]))

    async def test_search_filter(self):
        collection: Collection[AppleType] = self.client.collections["fruits"]
        result = await collection.documents.search(
            q="*", query_by=["name"], filter_by="color:red"
        )
        self.assertEqual(3, len(result["hits"]))

    async def test_search_facet(self):
        collection: Collection[AppleType] = self.client.collections["fruits"]
        result = await collection.documents.search(
            q="*", query_by=["name"], facet_by="color"
        )

        self.assertEqual(1, len(result["facet_counts"]))
        self.assertEqual(3, len(result["facet_counts"][0]["counts"]))
        self.assertEqual(7, result["found"])
