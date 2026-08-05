### create leads

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads-api#leads-add
- params:

|  name   | type | default value |
| :-----: | :--: | :-----------: |
| objects | list |       -       |

```python
objects = [
    {
        "name": "Сделка для примера 1",
        "created_by": 0,
        "price": 20000,
        "custom_fields_values": [
            {
                "field_id": 294471,
                "values": [
                    {
                        "value": "Наш первый клиент"
                    }
                ]
            }
        ]
    },
    {
        "name": "Сделка для примера 2",
        "price": 10000,
        "_embedded": {
            "tags": [
                {
                    "id": 2719
                }
            ]
        }
    }
]
result = client.create_leads(objects)
```

### update leads

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads-api#leads-edit
- params:

|  name   | type | default value |
| :-----: | :--: | :-----------: |
| objects | list |       -       |

```python
objects = [
    {
        "id": 54886,
        "pipeline_id": 47521,
        "status_id": 143,
        "date_close": 1589297221,
        "loss_reason_id": 7323,
        "updated_by": 0
    },
    {
        "id": 54884,
        "price": 50000,
        "pipeline_id": 47521,
        "status_id": 525743,
        "_embedded": {
            "tags": None
        }
    }
]
result = client.update_leads(objects)
```

### get lead

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads-api#lead-detail
- params:

|  name   | type | default value |
| :-----: | :--: | :-----------: |
| lead_id | int  |       -       |

```python
lead = client.get_lead(123)
```

### get leads

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads-api#leads-list
- params:

|    name     |      type      | default value |
| :---------: | :------------: | :-----------: |
|    limit    |      int       |      250      |
|    page     |      int       |       1       |
| with_params | Optional[list] |     None      |
|   filters   | Optional[dict] |     None      |
|    order    | Optional[dict] |     None      |

```python
leads = client.get_leads(limit=10, page=3, filters={'updated_at__from': '<timestamp>', 'updated_at__to': '<timestamp>'})
# for any timestamp fields like created_at, updated_at, closed_at u need to user __ like created_at__from, created_at__to
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    # leads = await client.get_leads_async(limit=10, filters={'updated_at__from': '<timestamp>'})
    await client.close_async()

asyncio.run(main())
```
