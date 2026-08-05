### get tags by entity type

- doc - https://www.amocrm.ru/developers/content/crm_platform/tags-api#tags-list

`entity_type` может быть `leads|contacts|companies|customers`

- params:

|    name     |      type      | default value |
| :---------: | :------------: | :-----------: |
| entity_type |      str       |       -       |
|    page     |      int       |       1       |
|    limit    |      int       |      250      |
|   filters   | Optional[dict] |     None      |

```python
tags = client.get_tags_by_entity_type('leads', page=1, limit=10)
```

### add tags for entity type

- doc - https://www.amocrm.ru/developers/content/crm_platform/tags-api#tags-add

`entity_type` может быть `leads|contacts|companies|customers`

- params:

|    name     | type | default value |
| :---------: | :--: | :-----------: |
| entity_type | str  |       -       |
|    tags     | list |       -       |

```python
tags = [
    {
        "name": "Tag 1"
    },
    {
        "name": "Tag 2",
        "request_id": "my_request_id"
    }
]
result = client.add_tags_for_entity_type('leads', tags=tags)
```

### iter tags by entity type

Пагинация через ленивый итератор по всем страницам:

```python
for tag in client.iter_tags_by_entity_type('leads'):
    print(tag["name"])
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    tags = await client.get_tags_by_entity_type_async('leads')
    async for tag in client.iter_tags_by_entity_type_async('leads'):
        print(tag["name"])
    await client.close_async()

asyncio.run(main())
```