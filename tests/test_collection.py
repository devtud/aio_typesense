from tests.common import collection_schema
from tests.docker_ import DockerTestCase


class TestCollections(DockerTestCase):
    async def test_collection_get_not_exists(self):
        collection = await self.client.collections["fruits"].retrieve()
        self.assertIsNone(collection)

    async def test_collections_get(self):
        created_col = await self.client.collections.create(collection_schema)
        self.assertIn("name", created_col)
        self.assertIn("fields", created_col)

        collection = await self.client.collections["fruits"].retrieve()

        self.assertEqual("fruits", collection["name"])
