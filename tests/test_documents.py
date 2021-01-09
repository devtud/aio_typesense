import asyncio
from unittest import mock

import httpx

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

    async def test_document_get_not_exists(self):
        doc = await self.client.collections["fruits"].documents["doc_id"].retrieve()
        self.assertIsNone(doc)

    async def test_document_get_ok(self):
        doc = {
            "id": "doc_id",
            "name": "Red Delicious",
            "timestamp": 23452345,
            "color": "red",
        }
        created_doc = await self.client.collections["fruits"].documents.create(doc)
        self.assertEqual(doc, created_doc)

        get_doc = await self.client.collections["fruits"].documents["doc_id"].retrieve()
        self.assertEqual(doc, get_doc)

    async def test_document_get_raises(self):
        document_obj = self.client.collections["fruits"].documents["doc_id"]

        with mock.patch.object(document_obj.api_call, "request") as mocked_request:
            mocked_request.side_effect = ValueError("error")

            with self.assertRaises(ValueError) as ctx:
                _ = await document_obj.retrieve()
            self.assertTrue(isinstance(ctx.exception, ValueError))

        with mock.patch.object(document_obj.api_call, "request") as mocked_request:
            httpx_response_mock = mock.Mock()
            httpx_response_mock.status_code = 300
            mocked_request.side_effect = httpx.HTTPStatusError(
                "msg", request=mock.Mock(), response=httpx_response_mock
            )

            with self.assertRaises(httpx.HTTPStatusError) as ctx:
                _ = await document_obj.retrieve()
            self.assertTrue(isinstance(ctx.exception, httpx.HTTPStatusError))

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

    async def test_document_delete(self):
        fruit = {
            "id": "doc_id",
            "name": "Red Delicious",
            "timestamp": 3253425,
            "color": "red",
        }

        created_doc = await self.client.collections["fruits"].documents.create(fruit)

        self.assertEqual(fruit, created_doc)

        deleted_doc = (
            await self.client.collections["fruits"].documents["doc_id"].delete()
        )

        self.assertEqual(fruit, deleted_doc)
