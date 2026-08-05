### get catalogs

- doc - https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#lists-list
- params:

| name  | type | default value |
| :---: | :--: | :-----------: |
| page  | int  |       1       |
| limit | int  |      250      |

```python
catalogs = client.get_catalogs(page=1, limit=5)
```

### get catalog

- doc - https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#list-detail
- params:

|    name    | type | default value |
| :--------: | :--: | :-----------: |
| catalog_id | int  |       1       |

```python
catalog = client.get_catalog(12319)
```

### create catalogs

- doc - https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#lists-add
- params:

|   name   | type | default value |
| :------: | :--: | :-----------: |
| catalogs | list |       -       |

```python
catalogs = [
    {
        "name": "Тестовый список",
        "can_add_elements": True,
        "can_link_multiple": False,
        "request_id": "123"
    }
]}
]
result = client.create_catalogs(catalogs)
```

### update catalogs

- doc - https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#lists-edit
- params:

|   name   | type | default value |
| :------: | :--: | :-----------: |
| catalogs | list |       -       |

```python
catalogs = [
    {
        "id": 5787,
        "name": "Новое имя списка",
        "can_add_elements": True,
        "can_link_multiple": False
    }
]
result = client.update_catalogs(catalogs)
```

### get elements from catalog

- doc - https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#list-elements-list
- params:

|    name     |      type      | default value |
| :---------: | :------------: | :-----------: |
| catalogs_id |      int       |       -       |
|    page     |      int       |       1       |
|    limit    |      int       |      250      |
|   filters   | Optional[dict] |     None      |

```python
elements = client.get_catalog_elements(5787, page=3, limit=8)
```

### get element from catalog

- doc - https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#list-elements-detail
- params:

|    name     | type | default value |
| :---------: | :--: | :-----------: |
| catalogs_id | int  |       -       |
| element_id  | int  |       -       |

```python
element = client.get_catalog_element(5787, 2301)
```

### add elements to catalog

- doc - https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#list-elements-add
- params:

|    name     | type | default value |
| :---------: | :--: | :-----------: |
| catalogs_id | int  |       -       |
|  elements   | list |       -       |

```python
elements = [
    {
        "name": "Новый элемент списка",
        "custom_fields_values": [
            {
                "field_id": 14263,
                "values": [
                    {
                        "value": 1000
                    }
                ]
            }
        ]
    }
]
result = client.add_elements_to_catalog(5787, elements)
```

### update elements in catalog

- doc - https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#list-elements-edit
- params:

|    name     | type | default value |
| :---------: | :--: | :-----------: |
| catalogs_id | int  |       -       |
|  elements   | list |       -       |

```python
elements = [
    {
        "id": 986757,
        "name": "Новое имя элемента"
    },
    {
        "id": 986753,
        "name": "Новое имя элемента 2"
    }
]
result = client.update_elements_in_catalog(5787, elements)
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    # elements = await client.get_catalog_elements_async(catalog_id=123)
    await client.close_async()

asyncio.run(main())
```
