### get tasks

- doc - https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-list
- params:

|  name   |      type      | default value |
| :-----: | :------------: | :-----------: |
|  page   |      int       |       1       |
|  limit  |      int       |      250      |
| filters | Optional[dict] |     None      |
|  order  | Optional[dict] |     None      |

```python
tasks = client.get_tasks(page=1, limit=10, filters={'updated_at__from': '<timestamp>', 'updated_at__to': '<timestamp>'})
# for any timestamp fields like created_at, updated_at, closed_at u need to user __ like created_at__from, created_at__to
```

### get task

- doc - https://www.amocrm.ru/developers/content/crm_platform/tasks-api#task-detail
- params:

|  name   | type | default value |
| :-----: | :--: | :-----------: |
| task_id | int  |       -       |

```python
task = client.get_task(1288)
```

### add tasks

- doc - https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-add
- params:

| name  | type | default value |
| :---: | :--: | :-----------: |
| tasks | list |       -       |

```python
tasks = [
    {
        "task_type_id": 1,
        "text": "Встретиться с клиентом Иван Иванов",
        "complete_till": 1588885140,
        "entity_id": 9785993,
        "entity_type": "leads",
        "request_id": "example"
    }
]
result = client.add_tasks(tasks=tasks)
```

### update tasks

- doc - https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-edit
- params:

| name  | type | default value |
| :---: | :--: | :-----------: |
| tasks | list |       -       |

```python
tasks = [
    {
        "id": 4745251,
        "task_type_id": 2,
        "text": "Новое название для задачи",
        "complete_till": 1588885140
    },
    {
        "id": 4747929,
        "task_type_id": 1,
        "text": "Новое название для задачи 2",
        "complete_till": 1588885140
    }
]
result = client.update_tasks(tasks=tasks)
```

### execution task

- doc - https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-complete
- params:

|     name     | type | default value |
| :----------: | :--: | :-----------: |
|   task_id    | int  |       -       |
| is_completed | bool |       -       |
|    result    | str  |       -       |

```python
result = client.execution_task(1288, is_completed=True, result="Удалось связаться с клиентом")
```

### get tasks by entity type (leads|contacts|companies|customers)

- doc - https://www.amocrm.ru/developers/content/crm_platform/tags-api#tags-list
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

### add tasks for entity type (leads|contacts|companies|customers)

- doc - https://www.amocrm.ru/developers/content/crm_platform/tags-api#tags-add
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
    },
    {
        "name": "Tag 3"
    }
]
tags = client.add_tags_for_entity_type('leads', tags=tags)
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    # tasks = await client.get_tasks_async(limit=10)
    await client.close_async()

asyncio.run(main())
```
