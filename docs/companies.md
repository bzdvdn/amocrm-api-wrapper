### get companies

- doc - https://www.amocrm.ru/developers/content/crm_platform/companies-api#companies-list
- params:

|    name     |      type      | default value |
| :---------: | :------------: | :-----------: |
|    limit    |      int       |      250      |
|    page     |      int       |       1       |
| with_params | Optional[list] |     None      |
|   filters   | Optional[dict] |     None      |
|    order    | Optional[dict] |     None      |

```python

companies = client.get_companies(limit=10, page=3, filters={'updated_at__from': '<timestamp>', 'updated_at__to': '<timestamp>'})
# for any timestamp fields like created_at, updated_at, closed_at u need to user __ like created_at__from, created_at__to
```

### get company

- doc - https://www.amocrm.ru/developers/content/crm_platform/companies-api#company-detail
- params:

|    name    | type | default value |
| :--------: | :--: | :-----------: |
| company_id | int  |       -       |

```python

company = client.get_company(9988)
```

### create companies

- doc - https://www.amocrm.ru/developers/content/crm_platform/companies-api#companies-add
- params:

|   name    | type | default value |
| :-------: | :--: | :-----------: |
| companies | list |       -       |

```python
companies = [
    {
        "name": "АО Рога и Копыта",
        "custom_fields_values": [
            {
                "field_code": "PHONE",
                "values": [
                    {
                        "value": "+7912322222",
                        "enum_code": "WORK"
                    }
                ]
            }
        ]
    }
]
result = client.create_companies(companies)
```

### update companies

- doc - https://www.amocrm.ru/developers/content/crm_platform/companies-api#companies-edit
- params:

|   name    | type | default value |
| :-------: | :--: | :-----------: |
| companies | list |       -       |

```python
companies = [
    {
        "id": 11090825,
        "name": "Новое название компании",
        "custom_fields_values": [
            {
                "field_code": "EMAIL",
                "values": [
                    {
                        "value": "test@example.com",
                        "enum_code": "WORK"
                    }
                ]
            }
       ]
    }
]
result = client.update_companies(companies)
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    # companies = await client.get_companies_async(limit=10)
    await client.close_async()

asyncio.run(main())
```
