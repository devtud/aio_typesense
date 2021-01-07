import logging
from typing import List, Union

import httpx


class ApiCall:
    def __init__(self, node_urls: List[str], api_key: str):
        self.node_urls = node_urls
        self.api_key = api_key

    async def request(
        self,
        *,
        method: str,
        endpoint: str,
        params: dict = None,
        data: Union[dict, list] = None,
    ) -> bytes:
        url = f"{self.node_urls[0]}/{endpoint.strip('/')}"
        headers = {
            "Content-Type": "application/json",
            "X-TYPESENSE-API-KEY": self.api_key,
        }

        async with httpx.AsyncClient() as http_client:
            r = await http_client.request(
                method=method, url=url, params=params, headers=headers, json=data
            )

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            logging.error(e.response.content)
            raise e

        return r.content