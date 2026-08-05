### get users

- doc - https://www.amocrm.ru/developers/content/crm_platform/users-api#users-list
- params:

|    name    | type | default value |
| :--------: | :--: | :-----------: |
|    page    | int  |       1       |
|   limit    | list |      250      |
| with_role  | bool |     False     |
| with_group | bool |     False     |

```python
users = client.get_users(page=1, limit=250)
```

### get user

- doc - https://www.amocrm.ru/developers/content/crm_platform/users-api#user-detail
- params:

|    name    | type | default value |
| :--------: | :--: | :-----------: |
|  user_id   | int  |       1       |
| with_role  | bool |     False     |
| with_group | bool |     False     |

```python
user = client.get_user(2222, with_role=True, with_group=True)
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    # users = await client.get_users_async()
    await client.close_async()

asyncio.run(main())
```
