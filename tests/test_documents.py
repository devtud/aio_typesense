import asyncio

from tests.common import collection_schema
from tests.docker_ import DockerTestCase


class TestDocuments(DockerTestCase):
    def setUp(self) -> None:
        super().setUp()
        loop = asyncio.get_event_loop()
        collection = loop.run_until_complete(
            self.client.collections.create(collection_schema)
        )
        self.assertEqual("fruits", collection["name"])

    async def test_documents_get_not_exists(self):
        doc = await self.client.collections["fruits"].documents["doc_id"].retrieve()
        self.assertIsNone(doc)

    async def test_documents_add(self):
        fruit = {
            "id": "doc_id",
            "name": "Red Delicious",
            "timestamp": 23452345,
            "color": "red",
        }
        doc = await self.client.collections["fruits"].documents.create(fruit)

        self.assertEqual(fruit, doc)

    async def test_document_add_update(self):
        fruit = {
            "id": "doc_id",
            "name": "Red Delicious",
            "timestamp": 3253425,
            "color": "red",
        }

        created_doc = await self.client.collections["fruits"].documents.create(fruit)

        self.assertEqual(fruit, created_doc)

        updated_doc = (
            await self.client.collections["fruits"]
            .documents["doc_id"]
            .update({"name": "Golden Delicious"})
        )
        self.assertEqual({"id": "doc_id", "name": "Golden Delicious"}, updated_doc)
