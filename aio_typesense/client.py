from typing import List

from aio_typesense.collections import Collections
from aio_typesense.api_call import ApiCall


class Client:
    def __init__(self, node_urls: List[str], api_key: str):
        self.collections: Collections = Collections(ApiCall(node_urls, api_key))
