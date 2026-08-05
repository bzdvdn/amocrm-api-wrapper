### get sources

- doc - https://www.amocrm.ru/developers/content/crm_platform/sources-api#sources-list
- params:

|    name     |      type      | default value |
| :---------: | :------------: | :-----------: |
|    page     |      int       |       1       |
|    limit    |      int       |      250      |
| with_params | Optional[list] |     None      |

```python
sources = client.get_sources(page=1, limit=10)
```

### get source

- doc - https://www.amocrm.ru/developers/content/crm_platform/sources-api#sources-detail
- params:

|   name    | type | default value |
| :-------: | :--: | :-----------: |
| source_id | int  |       -       |

```python
source = client.get_source(1876532)
```

### create sources

- doc - https://www.amocrm.ru/developers/content/crm_platform/sources-api#sources-add
- params:

|  name   | type | default value |
| :-----: | :--: | :-----------: |
| sources | list |       -       |

```python
sources = [
    {
        "name": "Виджет-сайт",
        "external_id": "site_widget"
    }
]
result = client.create_sources(sources)
```

### update sources

- doc - https://www.amocrm.ru/developers/content/crm_platform/sources-api#sources-edit
- params:

|  name   | type | default value |
| :-----: | :--: | :-----------: |
| sources | list |       -       |

```python
sources = [
    {
        "id": 1876532,
        "name": "Новое название канала"
    }
]
result = client.update_sources(sources)
```

### delete sources

- doc - https://www.amocrm.ru/developers/content/crm_platform/sources-api#sources-delete
- params:

|  name   | type | default value |
| :-----: | :--: | :-----------: |
| sources | list |       -       |

```python
sources = [
    {
        "id": 1876532
    }
]
result = client.delete_sources(sources)
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    sources = await client.get_sources_async(page=1, limit=10)
    await client.close_async()

asyncio.run(main())
```