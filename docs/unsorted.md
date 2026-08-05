### get unsorted leads

- doc - https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-list
- params:

|         name          |          type          | default value |
| :-------------------: | :--------------------: | :-----------: |
|         limit         |          int           |      250      |
|         page          |          int           |       1       |
|    filter_by_uids     | Union[str, list, None] |     None      |
| filter_by_pipeline_id | Union[str, list, None] |     None      |
|  filter_by_category   | Union[str, list, None] |     None      |
|       order_by        |     Optional[dict]     |     None      |

```python
unsorted_leads = client.get_unsorted_leads(limit=10, page=3, filter_by_pipeline_id=[1, 2310, 8751035])
```

### get unsorted lead by uid

- doc - https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-detail
- params:

| name | type | default value |
| :--: | :--: | :-----------: |
| uid  | str  |       -       |

```python
unsorted_lead = client.get_unsorted_by_uid('ufsigkgdjlk13igmd')
```

### create unsorted lead by sip

- doc - https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-add-sip
- params:

|    name     |     type      | default value |
| :---------: | :-----------: | :-----------: |
| source_uid  |      str      |       -       |
| source_name |      str      |       -       |
|  metadata   |     dict      |       -       |
|  conctact   |     dict      |       -       |
|    lead     |     dict      |       -       |
|  comapany   |     dict      |       -       |
| pipeline_id | Optional[int] |     None      |
| created_at  | Optional[int] |     None      |
| request_id  | Optional[int] |     None      |

```python
unsorted_lead = {
        "request_id": "123",
        "source_name": "ОАО Коспромсервис",
        "source_uid": "a1fee7c0fc436088e64ba2e8822ba2b3",
        "pipeline_id": 2194576,
        "created_at": 1510261200,
        "leads": {
                "name": "Тех обслуживание",
                "price": 5000,
                "custom_fields_values": [
                    {
                        "field_id": 284785,
                        "values": [
                            {
                                "value": "Кастомное поле"
                            }
                        ]
                    }
                ],
                "_embedded": {
                    "tags": [
                        {
                            "id": 263809
                        }
                    ]
                }
            }
        ],
        "contacts":
            {
                "name": "Контакт для примера"
            }
        "companies":
            {
                "name": "ОАО Коспромсервис"
            }
        },
        "metadata": {
            "is_call_event_needed": True,
            "uniq": "a1fe231cc88e64ba2e8822ba2b3ewrw",
            "duration": 54,
            "service_code": "CkAvbEwPam6sad",
            "link": "https://example.com",
            "phone": 79998888888,
            "called_at": 1510261200,
            "from": "onlinePBX"
        }
    }
result = client.create_unsorted_by_sip(**unsorted_lead)
```

### create unsorted lead by form

- doc - https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-add-form
- params:

|    name     |     type      | default value |
| :---------: | :-----------: | :-----------: |
| source_uid  |      str      |       -       |
| source_name |      str      |       -       |
|  metadata   |     dict      |       -       |
|  conctact   |     dict      |       -       |
|    lead     |     dict      |       -       |
|  comapany   |     dict      |       -       |
| pipeline_id | Optional[int] |     None      |
| created_at  | Optional[int] |     None      |
| request_id  | Optional[int] |     None      |

```python
unsorted_lead = {
        "request_id": "123",
        "source_name": "ОАО Коспромсервис",
        "source_uid": "a1fee7c0fc436088e64ba2e8822ba2b3",
        "pipeline_id": 2194576,
        "created_at": 1590830520,
        "leads": {
            "name": "Тех обслуживание",
            "visitor_uid": "5692210d-58d0-468c-acb2-dce7f93eef87",
            "price": 5000,
            "custom_fields_values": [
                {
                    "field_id": 284785,
                    "values": [
                        {
                            "value": "Дополнительное поле"
                        }
                    ]
                }
            ],
            "_embedded": {
                "tags": [
                    {
                        "name": "Тег для примера"
                    }
                ]
            }
        },
        "contacts":
            {
                "name": 234,
                "first_name": "123213",
                "last_name": 234,
                "custom_fields_values": [
                    {
                        "field_code": "PHONE",
                        "values": [
                            {
                                "value": "+7912321323"
                            }
                        ]
                    }
                ]
            },
        "companies": {
            "name": "ОАО Коспромсервис"
        },
        "metadata": {
            "ip": "123.222.2.22",
            "form_id": "a1fee7c0fc436088e64ba2e8822ba2b3ewrw",
            "form_sent_at": 1590830520,
            "form_name": "Форма заявки для полёта в космос",
            "form_page": "https://example.com",
            "referer": "https://www.google.com/search?&q=elon+musk"
        }
    }
result = client.create_unsorted_by_form(**unsorted_lead)
```

### accept unsorted lead

- doc - https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-accept
- params:

|   name    | type | default value |
| :-------: | :--: | :-----------: |
|    uid    | str  |       -       |
|  user_id  | int  |       -       |
| status_id | int  |       -       |

```python
result = client.accept_unsorted('jkjsoijg2321kgkdu2', 2310, 4444)
```

### decline unsorted lead

- doc - https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-decline
- params:

|  name   | type | default value |
| :-----: | :--: | :-----------: |
|   uid   | str  |       -       |
| user_id | int  |       -       |

```python
result = client.decline_unsorted('jkjsoijg2321kgkdu2', 2310,)
```

### link unsorted lead ot another lead

- doc - https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-link
- params:

|  name   | type | default value |
| :-----: | :--: | :-----------: |
|   uid   | str  |       -       |
| user_id | int  |       -       |
|  link   | dict |       -       |

```python
result = client.link_unsorted('jkjsoijg2321kgkdu2', 2310, link={
    "entity_id": 93144801,
    "entity_type": "leads"
})
```

### get summary unsorted leads

- doc - https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-summary
- params:

|        name        |          type          | default value |
| :----------------: | :--------------------: | :-----------: |
|        uid         | Union[str, list, None] |     None      |
| created_at\_\_from |     Optional[str]      |     None      |
|  created_at\_\_to  |     Optional[str]      |     None      |
|    pipeline_id     | Union[str, list, None] |     None      |

```python
summary_unsorted = client.get_summary_unsorted()
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    # unsorted_leads = await client.get_unsorted_leads_async(limit=10, filter_by_pipeline_id=[1, 2310])
    await client.close_async()

asyncio.run(main())
```
