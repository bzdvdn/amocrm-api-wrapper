### get loss reasons

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads-api#loss-reasons-list
- params:

|    name     |      type      | default value |
| :---------: | :------------: | :-----------: |
|    page     |      int       |       1       |
|    limit    |      int       |      250      |
| with_params | Optional[list] |     None      |

```python
loss_reasons = client.get_loss_reasons(page=1, limit=10)
```

### get loss reason

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads-api#loss-reasons-detail
- params:

|      name      | type | default value |
| :------------: | :--: | :-----------: |
| loss_reason_id | int  |       -       |

```python
loss_reason = client.get_loss_reason(4203748)
```

### create loss reasons

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads-api#loss-reasons-add
- params:

|     name     | type | default value |
| :----------: | :--: | :-----------: |
| loss_reasons | list |       -       |

```python
loss_reasons = [
    {
        "name": "Пропала потребность"
    },
    {
        "name": "Не сошлись в цене"
    }
]
result = client.create_loss_reasons(loss_reasons)
```

### update loss reasons

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads-api#loss-reasons-edit
- params:

|     name     | type | default value |
| :----------: | :--: | :-----------: |
| loss_reasons | list |       -       |

```python
loss_reasons = [
    {
        "id": 4203748,
        "name": "Не сошлись в цене"
    }
]
result = client.update_loss_reasons(loss_reasons)
```

### delete loss reason

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads-api#loss-reasons-delete
- params:

|      name      | type | default value |
| :------------: | :--: | :-----------: |
| loss_reason_id | int  |       -       |

```python
result = client.delete_loss_reason(4203748)
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    loss_reasons = await client.get_loss_reasons_async(page=1, limit=10)
    await client.close_async()

asyncio.run(main())
```