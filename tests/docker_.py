import asyncio
import uuid
from time import sleep
from typing import List
from unittest.async_case import IsolatedAsyncioTestCase

import docker
from docker.models.containers import Container

from aio_typesense import Client
from tests.common import get_api_key

TYPESENSE_DOCKER_IMAGE = "typesense/typesense:0.18.0"


class DockerTestCase(IsolatedAsyncioTestCase):

    container: Container = None
    client: Client = None

    @classmethod
    def setUpClass(cls) -> None:
        """ Before each test class create meili container """
        api_key = get_api_key()
        cls.container = start_container(api_key=api_key)
        cls.client = Client(node_urls=["http://localhost:8108"], api_key=api_key)
        sleep(1)

    @classmethod
    def tearDownClass(cls) -> None:
        """ After each test class destroy the container"""
        cls.container.kill()
        cls.container.remove()
        cls.container.client.close()

    def setUp(self) -> None:
        self.maxDiff = None

    def tearDown(self) -> None:
        """ After each test method remove all indexes from meili db"""
        loop = asyncio.get_event_loop()
        collections: List[dict] = loop.run_until_complete(
            self.client.collections.retrieve()
        )
        for collection in collections:
            loop.run_until_complete(
                self.client.collections[collection["name"]].delete()
            )

        collections = loop.run_until_complete(self.client.collections.retrieve())
        self.assertEqual(0, len(collections))


def start_container(
    api_key: str, docker_base_url: str = "unix://var/run/docker.sock"
) -> Container:
    docker_client = docker.DockerClient(base_url=docker_base_url, version="auto")

    docker_client.api.pull(TYPESENSE_DOCKER_IMAGE)

    container: Container = docker_client.containers.create(
        image=TYPESENSE_DOCKER_IMAGE,
        command=[
            "--api-key=" + api_key,
            "--data-dir=/data",
        ],
        name=f"test-typesense-{uuid.uuid4()}",
        detach=True,
        ports={8108: 8108},
        volumes={"/tmp/typesense-data": {"bind": "/data", "mode": "rw"}},
    )
    container.start()

    return container
