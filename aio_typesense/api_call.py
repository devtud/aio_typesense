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
        data: Union[dict, list, bytes] = None,
    ) -> bytes:
        url = f"{self.node_urls[0]}/{endpoint.strip('/')}"
        headers = {
            "Content-Type": "application/json",
            "X-TYPESENSE-API-KEY": self.api_key,
        }

        if isinstance(data, bytes):
            data_ = {"content": data}
        else:
            data_ = {"json": data}

        http_client: httpx.AsyncClient

        async with httpx.AsyncClient() as http_client:
            r: httpx.Response = await http_client.request(
                method=method, url=url, params=params, headers=headers, **data_
            )

        r.raise_for_status()

        return r.content
