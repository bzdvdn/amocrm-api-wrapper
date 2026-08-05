### get notes by entity type

- doc - https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#notes-entity-list
- params:

|           name            |              type              | default value |
| :-----------------------: | :----------------------------: | :-----------: |
|       entity_type         |              str               |       -       |
|           page            |              int               |       1       |
|           limit           |              int               |      250      |
|       filter_by_id        |   Union[int, list, None]       |     None      |
|    filter_by_entity_id    |      Optional[list]            |     None      |
|    filter_by_note_type    |   Union[list, str, None]       |     None      |
|   filter_by_updated_at    |         Optional[int]          |     None      |
| filter_by_updated_at_from |         Optional[int]          |     None      |
|  filter_by_updated_at_to  |         Optional[int]          |     None      |
|    order_by_updated_at    |              str               |     asc       |
|       order_by_id         |              str               |     asc       |

```python
notes = client.get_notes_by_entity_type('leads', page=1, limit=10)
```

### get notes by entity type and entity id

- doc - https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#notes-entity-list
- params:

|           name            |              type               | default value |
| :-----------------------: | :-----------------------------: | :-----------: |
|       entity_type         |               str               |       -       |
|        entity_id          |               int               |       -       |
|           page            |               int               |       1       |
|           limit           |               int               |      250      |
|       filter_by_id        |    Union[int, list, None]       |     None      |
|    filter_by_note_type    |    Union[list, str, None]       |     None      |
|   filter_by_updated_at    |          Optional[int]          |     None      |
| filter_by_updated_at_from |          Optional[int]          |     None      |
|  filter_by_updated_at_to  |          Optional[int]          |     None      |
|    order_by_updated_at    |               str               |     asc       |
|       order_by_id         |               str               |     asc       |

```python
notes = client.get_notes_by_entity_type_and_entity_id('leads', 26050861, page=1, limit=10)
```

### get entity note

- doc - https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#note-detail
- params:

|    name     |        type        | default value |
| :---------: | :----------------: | :-----------: |
| entity_type |        str         |       -       |
|    id_      |        int         |       -       |
|  entity_id  | Optional[int]      |     None      |

```python
note = client.get_entity_note('leads', 42709325, entity_id=26050861)
```

### create entity note

- doc - https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#notes-add
- params:

|    name     |        type        | default value |
| :---------: | :----------------: | :-----------: |
| entity_type |        str         |       -       |
|    notes    |        list        |       -       |
|  entity_id  | Optional[int]      |     None      |

```python
notes = [
    {
        "note_type": "common",
        "params": {
            "text": "Текст примечания"
        }
    }
]
result = client.create_entity_note('leads', notes, entity_id=26050861)
```

### update entity note

- doc - https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#notes-edit
- params:

|    name     | type | default value |
| :---------: | :--: | :-----------: |
| entity_type | str  |       -       |
|  entity_id  | int  |       -       |
|    id_      | int  |       -       |
|   params    | dict |       -       |

```python
params = {
    "params": {
        "text": "Обновлённый текст"
    }
}
result = client.update_entity_note('leads', 26050861, 42709325, params)
```

### update entity many notes

- doc - https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#notes-edit
- params:

|    name     |        type        | default value |
| :---------: | :----------------: | :-----------: |
| entity_type |        str         |       -       |
|    notes    |        list        |       -       |
|  entity_id  | Optional[int]      |     None      |

```python
notes = [
    {
        "id": 42709325,
        "params": {
            "text": "Обновлённый текст"
        }
    }
]
result = client.update_entity_many_notes('leads', notes, entity_id=26050861)
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    notes = await client.get_notes_by_entity_type_async('leads', page=1, limit=10)
    await client.close_async()

asyncio.run(main())
```