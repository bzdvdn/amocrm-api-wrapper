## get account info

- doc - https://www.amocrm.ru/developers/content/crm_platform/account-info
- params:

|          name          | type | default value |
| :--------------------: | :--: | :-----------: |
|     with_amojo_id      | bool |     False     |
|   with_amojo_rights    | bool |     False     |
|   with_users_groups    | bool |     False     |
|    with_task_types     | bool |     False     |
|      with_version      | bool |     False     |
|   with_ventity_names   | bool |     False     |
| with_datetime_settings | bool |     False     |

```python
account_info = client.get_account_info()
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    # account_info = await client.get_account_info_async()
    await client.close_async()

asyncio.run(main())
```
