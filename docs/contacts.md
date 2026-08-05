### get contacts

- doc - https://www.amocrm.ru/developers/content/crm_platform/contacts-api#contacts-list
- params:

|    name     |      type      | default value |
| :---------: | :------------: | :-----------: |
|    limit    |      int       |      250      |
|    page     |      int       |       1       |
| with_params | Optional[list] |     None      |
|   filters   | Optional[dict] |     None      |
|    order    | Optional[dict] |     None      |

```python

contacts = client.get_contacts(limit=10, page=3, filters={'updated_at__from': '<timestamp>', 'updated_at__to': '<timestamp>'})
# for any timestamp fields like created_at, updated_at, closed_at u need to user __ like created_at__from, created_at__to
```

### get contact

- doc - https://www.amocrm.ru/developers/content/crm_platform/contacts-api#contact-detail
- params:

|    name    | type | default value |
| :--------: | :--: | :-----------: |
| contact_id | int  |       -       |

```python

contact = client.get_contact(123989)
```

### create contacts

- doc - https://www.amocrm.ru/developers/content/crm_platform/contacts-api#contacts-add
- params:

|   name   | type | default value |
| :------: | :--: | :-----------: |
| contacts | list |       -       |

```python
conctacts = [
    {
        "first_name": "Петр",
        "last_name": "Смирнов",
        "custom_fields_values": [
            {
                "field_id": 271316,
                "values": [
                    {
                        "value": "Директор"
                    }
                ]
            }
        ]
    },
    {
        "name": "Владимир Смирнов",
        "created_by": 47272
    }
]
result = client.create_contacts(contacts)
```

### update contacts

- doc - https://www.amocrm.ru/developers/content/crm_platform/contacts-api#contacts-edit
- params:

|   name   | type | default value |
| :------: | :--: | :-----------: |
| contacts | list |       -       |

```python
conctacts = [
    {
        "id": 3,
        "first_name": "Иван",
        "last_name": "Иванов",
        "custom_fields_values": [
            {
                "field_id": 66192,
                "field_name": "Телефон",
                "values": [
                    {
                        "value": "79999999999",
                        "enum_code": "WORK"
                    }
                ]
            }
       ]
    }
]
result = client.update_contacts(contacts)
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    # contacts = await client.get_contacts_async(limit=10)
    await client.close_async()

asyncio.run(main())
```
