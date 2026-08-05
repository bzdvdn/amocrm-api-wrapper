### get customers links

- doc - https://www.amocrm.ru/developers/content/crm_platform/entity-links-api#links-list
- params:

|   name    |      type      | default value |
| :-------: | :------------: | :-----------: |
| entity_id |      int       |       -       |
|  filters  | Optional[dict] |     None      |

```python
links = client.get_customers_links(123)
```

### link customers entity

- doc - https://www.amocrm.ru/developers/content/crm_platform/entity-links-api#links-link
- params:

|   name    | type | default value |
| :-------: | :--: | :-----------: |
| entity_id | int  |       -       |
|  objects  | list |       -       |

```python
objects = [
    {
        "to_entity_id": 7,
        "to_entity_type": "contacts"
    }
]
result = client.link_customers_entity(123, objects)
```

### unlink customers entity

- doc - https://www.amocrm.ru/developers/content/crm_platform/entity-links-api#links-unlink
- params:

|   name    | type | default value |
| :-------: | :--: | :-----------: |
| entity_id | int  |       -       |
|  objects  | list |       -       |

```python
objects = [
    {
        "to_entity_id": 7,
        "to_entity_type": "contacts"
    }
]
result = client.unlink_customers_entity(123, objects)
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    links = await client.get_customers_links_async(123)
    await client.close_async()

asyncio.run(main())
```
