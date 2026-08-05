### get chats

- doc - https://www.amocrm.ru/developers/content/crm_platform/chats-api#chats-list
- params:

|           name           |        type         | default value |
| :----------------------: | :-----------------: | :-----------: |
|           page           |         int         |       1       |
|          limit           |         int         |      250      |
|      filter_by_ids       | Union[int, list, None] |    None      |
| filter_by_created_at_from|      Optional[int]  |     None      |
| filter_by_created_at_to  |      Optional[int]  |     None      |
|       with_params        |     Optional[list]  |     None      |

```python
chats = client.get_chats(page=1, limit=10)
```

### get chat

- doc - https://www.amocrm.ru/developers/content/crm_platform/chats-api#chats-detail
- params:

|  name   | type | default value |
| :-----: | :--: | :-----------: |
| chat_id | int  |       -       |

```python
chat = client.get_chat(12345)
```

### create chats

- doc - https://www.amocrm.ru/developers/content/crm_platform/chats-api#chats-add
- params:

| name  | type | default value |
| :---: | :--: | :-----------: |
| chats | list |       -       |

```python
chats = [
    {
        "conversation_id": "conv-123",
        "source_id": 1876532
    }
]
result = client.create_chats(chats)
```

### update chat

- doc - https://www.amocrm.ru/developers/content/crm_platform/chats-api#chats-edit
- params:

|   name   | type | default value |
| :------: | :--: | :-----------: |
| chat_id  | int  |       -       |
|   chat   | dict |       -       |

```python
chat = {
    "source_id": 1876532
}
result = client.update_chat(12345, chat)
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    chats = await client.get_chats_async(page=1, limit=10)
    await client.close_async()

asyncio.run(main())
```