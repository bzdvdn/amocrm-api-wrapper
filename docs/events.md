### get events types

- doc - https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#events-types
- params:

|     name      |      type      | default value |
| :-----------: | :------------: | :-----------: |
| language_code | Optional[str]  |     None      |

```python
event_types = client.get_events_type()
```

### get events

- doc - https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#events-list
- params:

|           name           |           type            | default value |
| :----------------------: | :-----------------------: | :-----------: |
|           page           |            int            |       1       |
|          limit           |            int            |      250      |
|       with_params        |      Optional[list]       |     None      |
|       filter_by_ids      | Union[str, list, None]    |     None      |
| filter_by_created_from   | Union[str, list, None]    |     None      |
|  filter_by_created_to    | Union[str, list, None]    |     None      |
|  filter_by_created_by    | Union[str, list, None]    |     None      |
|    filter_by_entity      | Union[str, list, None]    |     None      |
|   filter_by_entity_id    | Union[str, list, None]    |     None      |
|      filter_by_type      | Union[str, list, None]    |     None      |

```python
events = client.get_events(page=1, limit=10, filter_by_type='lead_added')
```

### get event

- doc - https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#events-detail
- params:

|    name     |      type      | default value |
| :---------: | :------------: | :-----------: |
|     id      |      int       |       -       |
| with_params | Optional[list] |     None      |

```python
event = client.get_event('01pz58t6p04ymgsgfbmfyfy1mf')
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    events = await client.get_events_async(page=1, limit=10)
    await client.close_async()

asyncio.run(main())
```
