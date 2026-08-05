### get pipelines

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipelines-list

```python
pipelines = client.get_pipelines()
```

### craete pipeline

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipelines-add
- params:

|      name      |     type      | default value |
| :------------: | :-----------: | :-----------: |
|      name      |      str      |       -       |
|      sort      |      int      |       -       |
|    is_main     |     bool      |       -       |
|    statuses    |     list      |       -       |
| is_unsorted_on |     bool      |     False     |
|   request_id   | Optional[str] |     None      |

```python
pipeline = {
    "name": "Воронка доп продаж",
    "is_main": False,
    "is_unsorted_on": True,
    "sort": 20,
    "request_id": "123",
    "statuses": [
        {
            "id": 142,
            "name": "Мое название для успешных сделок"
        },
        {
            "name": "Первичный контакт",
            "sort": 10,
            "color": "#fffeb2"
        }
    ]
}
result = client.create_pipeline(**pipeline)
```

### edit pipeline

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipelines-add
- params:

|      name      | type | default value |
| :------------: | :--: | :-----------: |
|  pipeline_id   | int  |       -       |
|      name      | str  |       -       |
|      sort      | int  |       -       |
|    is_main     | bool |       -       |
| is_unsorted_on | bool |     False     |

```python
pipeline = {
    "pipeline_id": 2310,
    "name": "Новое название для воронки",
    "is_main": False,
    "is_unsorted_on": False,
    "sort": 100
}
result = client.edit_pipeline(**pipeline)
```

### delete pipeline

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipeline-delete
- params:

|    name     | type | default value |
| :---------: | :--: | :-----------: |
| pipeline_id | int  |       -       |

```python
result = client.delete_pipeline(2310)
```

### get statuses by pipeline

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#statuses-list
- params:

|    name     | type | default value |
| :---------: | :--: | :-----------: |
| pipeline_id | int  |       -       |

```python
pipeline_statuses = client.get_pipeline_statuses(2310)
```

### get pipeline status

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#status-detail
- params:

|    name     | type | default value |
| :---------: | :--: | :-----------: |
| pipeline_id | int  |       -       |
|  status_id  | int  |       -       |

```python
pipeline_status = client.get_pipeline_status(2310, 123)
```

### add statuses to pipeline

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#statuses-add
- params:

|    name     | type | default value |
| :---------: | :--: | :-----------: |
| pipeline_id | int  |       -       |
|  statuses   | list |       -       |

```python
statuses = [
    {
        "name": "Новый этап",
        "sort": 100,
        "color": "#fffeb2"
    },
    {
        "name": "Новый этап 2",
        "sort": 200,
        "color": "#fffeb2"
    }
]
result = client.add_statuses_to_pipeline(2310, statuses)
```

### edit pipeline status

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#statuses-add
- params:

|    name     | type | default value |
| :---------: | :--: | :-----------: |
| pipeline_id | int  |       -       |
|  status_id  | int  |       -       |
|    name     | str  |       -       |
|    sort     | int  |       -       |
|    color    | str  |       -       |

```python
result = client.edit_pipeline_status(2310, 123, 'Новый Этап', sort=500, color="#fffeb2")
```

### delete status from pipeline

- doc - https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#status-delete
- params:

|    name     | type | default value |
| :---------: | :--: | :-----------: |
| pipeline_id | int  |       -       |
|  status_id  | int  |       -       |

```python

result = client.delete_status_from_pipeline(2310, 123)
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    # pipelines = await client.get_pipelines_async()
    await client.close_async()

asyncio.run(main())
```
