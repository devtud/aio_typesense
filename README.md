[![Tests](https://github.com/devtud/aio_typesense/workflows/Tests/badge.svg)](https://github.com/devtud/aio_typesense/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/devtud/aio_typesense/branch/main/graph/badge.svg)](https://codecov.io/gh/devtud/aio_typesense)
![pypi](https://img.shields.io/pypi/v/aio_typesense.svg)
![versions](https://img.shields.io/pypi/pyversions/aio_typesense.svg)
[![](https://pypip.in/license/aio_typesense/badge.svg)](https://pypi.python.org/pypi/aio_typesense)

# aio_typesense
## Async Library for Typesense with type hints

```bash
pip install aio_typesense
```

## Usage

```python
# examples/example.py

import asyncio
from typing import TypedDict, List

from aio_typesense import Client, Collection


class Movie(TypedDict):
    id: str
    name: str
    year: int


MOVIES: List[Movie] = [
    {"id": "id1", "name": "Wonder Woman", "year": 2017, "year_facet": "2017"},
    {"id": "id2", "name": "Justice League", "year": 2017, "year_facet": "2017"},
    {"id": "id3", "name": "Wonder Woman 1984", "year": 2020, "year_facet": "2020"},
    {"id": "id4", "name": "Death on the Nile", "year": 2021, "year_facet": "2021"},
]


async def main():
    client = Client(
        node_urls=["http://localhost:8108"],
        api_key="Rhsdhas2asasdasj2",
    )

    r = await client.collections.create(
        {
            "name": "movies",
            "num_documents": 0,
            "fields": [
                {
                    "name": "name",
                    "type": "string",
                },
                {
                    "name": "year",
                    "type": "int32",
                },
                {
                    "name": "year_facet",
                    "type": "string",
                    "facet": True,
                },
            ],
            "default_sorting_field": "year",
        }
    )

    collection: Collection[Movie] = client.collections["movies"]

    r = await collection.documents.create_many(documents=MOVIES)
    print(r)

    search_r = await collection.documents.search(
        {
            "q": "wonder woman 2021",
            "query_by": "year_facet,name",
            "query_by_weights": "1,1",
        }
    )

    print(search_r["hits"])

    # [
    #     {
    #         "document": {
    #             "id": "id3",
    #             "name": "Wonder Woman 1984",
    #             "year": 2020,
    #             "year_facet": "2020",
    #         },
    #         "highlights": [
    #             {
    #                 "field": "year_facet",
    #                 "matched_tokens": ["2020"],
    #                 "snippet": "<mark>2020</mark>",
    #             }
    #         ],
    #         "text_match": 1125899907169635,
    #     },
    #     {
    #         "document": {
    #             "id": "id1",
    #             "name": "Wonder Woman",
    #             "year": 2017,
    #             "year_facet": "2017",
    #         },
    #         "highlights": [
    #             {
    #                 "field": "year_facet",
    #                 "matched_tokens": ["2017"],
    #                 "snippet": "<mark>2017</mark>",
    #             }
    #         ],
    #         "text_match": 1125899907169379,
    #     },
    #     {
    #         "document": {
    #             "id": "id4",
    #             "name": "Death on the Nile",
    #             "year": 2021,
    #             "year_facet": "2021",
    #         },
    #         "highlights": [
    #             {
    #                 "field": "year_facet",
    #                 "matched_tokens": ["2021"],
    #                 "snippet": "<mark>2021</mark>",
    #             }
    #         ],
    #         "text_match": 562949953552128,
    #     },
    #     {
    #         "document": {
    #             "id": "id2",
    #             "name": "Justice League",
    #             "year": 2017,
    #             "year_facet": "2017",
    #         },
    #         "highlights": [
    #             {
    #                 "field": "year_facet",
    #                 "matched_tokens": ["2017"],
    #                 "snippet": "<mark>2017</mark>",
    #             }
    #         ],
    #         "text_match": 562949953551616,
    #     },
    # ]


if __name__ == "__main__":
    asyncio.run(main())

```

## Contributing

**Prerequisites:**
 - **poetry**
 - **nox**
 - **nox-poetry**

Install them on your system:
```bash
pip install poetry nox nox-poetry
```

Run tests:
```bash
nox
```
