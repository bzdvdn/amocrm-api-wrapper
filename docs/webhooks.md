### get webhooks

- doc - https://www.amocrm.ru/developers/content/crm_platform/webhooks-api#webhooks-list
- params:

|    name    |     type      | default value |
| :--------: | :-----------: | :-----------: |
| distansion | Optional[str] |     None      |

```python
webhooks = client.get_webhooks()
```

### subscribe webhook

- doc - https://www.amocrm.ru/developers/content/crm_platform/webhooks-api#webhook-subscribe
- params:

|    name    | type | default value |
| :--------: | :--: | :-----------: |
| distansion | str  |       -       |
|  settings  | list |       -       |

```python
result = client.subscribe_webhook(destination="https://example.test", settings=["add_lead"])
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    # webhooks = await client.get_webhooks_async()
    await client.close_async()

asyncio.run(main())
```
