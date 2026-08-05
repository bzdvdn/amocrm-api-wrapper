### get widgets

- doc - https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widgets-list
- params:

| name  | type | default value |
| :---: | :--: | :-----------: |
| page  | int  |       1       |
| limit | int  |      250      |

```python
widgets = client.get_widgets(page=3, limit=22)
```

### get widget

- doc - https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widget-detail
- params:

|    name     | type | default value |
| :---------: | :--: | :-----------: |
| widget_code | str  |       -       |

```python
widget = client.get_widget('<widget_code>')
```

### install widget

- doc - https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widget-install
- params:

|    name     | type | default value |
| :---------: | :--: | :-----------: |
| widget_code | str  |       -       |
| \*\*kwargs  | str  |       -       |

```python
example ={
    "login": "example",
    "password": "eXaMp1E",
    "phones": {
        504141: "1039"
    },
    "script_path": "https://example.com/"
}
result = client.install_widget('<widget_code>', **example)
```

### uninstall widget

- doc - https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widget-uninstall
- params:

|    name     | type | default value |
| :---------: | :--: | :-----------: |
| widget_code | str  |       -       |

```python
result = client.uninstall_widget('<widget_code>')
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    # widgets = await client.get_widgets_async()
    await client.close_async()

asyncio.run(main())
```
