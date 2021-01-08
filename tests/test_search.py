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
        print("---created many", result)

    async def test_search_general(self):
        collection: Collection[AppleType] = self.client.collections["fruits"]
        result = await collection.documents.search(
            {
                "q": "apple",
                "query_by": ["name"],
            }
        )
        self.assertEqual(2, len(result["hits"]))
