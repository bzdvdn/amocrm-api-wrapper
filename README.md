# wrapper for amocrm rest api

## Install
Install using `pip`...

    pip install amocrm-api-wrapper


## Usage
=======
```python
from amocrm_api import AmoLegacyClient # for login password auth
from amocrm_api import AmoOAuthClient # for oauth
from datetime import datetime

client = AmoLegacyClient('<login>', '<password>', '<crm_url>')
client = AmoOAuthClient('<access_token>', '<refresh_token>', '<crm_url>', '<client_id>', '<client_secret>', '<redirect_uri>')
dt = datetime.datetime.today().strftime("%a, %d %b %Y %H-%m-%d")
date_time = f"{dt} UTC"

# for Legacy client
headers = {
    "IF-MODIFIED-SINCE": f"{date_time}",
    "Content-Type": "application/json",
}

client.update_session_params(headers)
```
### get account info
* doc - https://www.amocrm.ru/developers/content/crm_platform/account-info   
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| with_amojo_id     |  bool  | False |
| with_amojo_rights     |  bool  | False |
| with_users_groups     |  bool  | False |
| with_task_types     |  bool  | False |
| with_version     |  bool  | False |
| with_ventity_names     |  bool  | False |
| with_datetime_settings     |  bool  | False |
```python
account_info = client.get_account_info()
```

### create leads
* doc - https://www.amocrm.ru/developers/content/crm_platform/leads-api#leads-add  
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| objects     |  list  | - |
```python
objects = [
    {
        "name": "Сделка для примера 1",
        "created_by": 0,
        "price": 20000,
        "custom_fields_values": [
            {
                "field_id": 294471,
                "values": [
                    {
                        "value": "Наш первый клиент"
                    }
                ]
            }
        ]
    },
    {
        "name": "Сделка для примера 2",
        "price": 10000,
        "_embedded": {
            "tags": [
                {
                    "id": 2719
                }
            ]
        }
    }
]
result = client.create_leads(objects)
```
### update leads
* doc - https://www.amocrm.ru/developers/content/crm_platform/leads-api#leads-edit  
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| objects     |  list  | - |
```python
objects = [
    {
        "id": 54886,
        "pipeline_id": 47521,
        "status_id": 143,
        "date_close": 1589297221,
        "loss_reason_id": 7323,
        "updated_by": 0
    },
    {
        "id": 54884,
        "price": 50000,
        "pipeline_id": 47521,
        "status_id": 525743,
        "_embedded": {
            "tags": None
        }
    }
]
result = client.update_leads(objects)
```
### get lead
* doc - https://www.amocrm.ru/developers/content/crm_platform/leads-api#lead-detail 
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| lead_id     |  int  | - |
```python
lead = client.get_lead(123)
```
### get leads
* doc - https://www.amocrm.ru/developers/content/crm_platform/leads-api#leads-list
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| limit     |  int  | 250 |
| page     |  int  | 1 |
| with_params     |  Optional[list]  | None |
| filters     |  Optional[dict]  | None |
| order     |  Optional[dict]  | None |
```python
leads = client.get_leads(limit=10, page=3, filters={'[updated_at][from]': '<timestamp>'})
```
### get unsorted leads
* doc - https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-list
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| limit     |  int  | 250 |
| page     |  int  | 1 |
| filter_by_uids     |  Union[str, list, None] | None |
| filter_by_pipeline_id     |  Union[str, list, None] | None |
| filter_by_category     |  Union[str, list, None] | None |
| order_by     |  Optional[dict] | None |
```python
unsorted_leads = client.get_unsorted_leads(limit=10, page=3, filter_by_pipeline_id=[1, 2310, 8751035])
```
### get unsorted lead by uid
* doc - https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-detail
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| uid     |  str  | - |

```python
unsorted_lead = client.get_unsorted_by_uid('ufsigkgdjlk13igmd')
```
### create unsorted lead by sip
* doc - https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-add-sip
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| source_uid     |  str  | - |
| source_name     |  str  | - |
| metadata     |  dict  | - |
| conctact     |  dict  | - |
| lead     |  dict  | - |
| comapany     |  dict  | - |
| pipeline_id     |  Optional[int]  | None |
| created_at     |  Optional[int]  | None |
| request_id     |  Optional[int]  | None |

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
* doc - https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-add-form
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| source_uid     |  str  | - |
| source_name     |  str  | - |
| metadata     |  dict  | - |
| conctact     |  dict  | - |
| lead     |  dict  | - |
| comapany     |  dict  | - |
| pipeline_id     |  Optional[int]  | None |
| created_at     |  Optional[int]  | None |
| request_id     |  Optional[int]  | None |

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
* doc -  https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-accept
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| uid     |  str  | - |
| user_id     |  int  | - |
| status_id     |  int  | - |
```python
result = client.accept_unsorted('jkjsoijg2321kgkdu2', 2310, 4444)
```
### decline unsorted lead
* doc -  https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-decline
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| uid     |  str  | - |
| user_id     |  int  | - |
```python
result = client.decline_unsorted('jkjsoijg2321kgkdu2', 2310,)
```

### link unsorted lead ot another lead
* doc -  https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-link
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| uid     |  str  | - |
| user_id     |  int  | - |
| link     |  dict  | - |
```python
result = client.link_unsorted('jkjsoijg2321kgkdu2', 2310, link={
    "entity_id": 93144801,
    "entity_type": "leads"
})
```
### get summary unsorted leads
* doc -  https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-summary
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| uid     |  Union[str, list, None] | None |
| created_at__from     |  Optional[str]  | None |
| created_at__to     |  Optional[str]  | None |
| pipeline_id     |  Union[str, list, None] | None |
```python
summary_unsorted = client.get_summary_unsorted()
```
### get pipelines
* doc -  https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipelines-list
```python
pipelines = client.get_pipelines()
```
### craete pipeline
* doc -  https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipelines-add
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| name     |  str | - |
| sort     |  int | - |
| is_main     |  bool | - |
| statuses     |  list | - |
| is_unsorted_on     |  bool | False |
| request_id     |  Optional[str] | None |

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
* doc -  https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipelines-add
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| pipeline_id     |  int | - |
| name     |  str | - |
| sort     |  int | - |
| is_main     |  bool | - |
| is_unsorted_on     |  bool | False |

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
* doc -  https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipeline-delete
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| pipeline_id     |  int | - |

```python
result = client.delete_pipeline(2310)
```
### get statuses by pipeline
* doc -  https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#statuses-list
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| pipeline_id     |  int | - |
```python
pipeline_statuses = client.get_pipeline_statuses(2310)
```
### get pipeline status
* doc -  https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#status-detail
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| pipeline_id     |  int | - |
| status_id     |  int | - |
```python
pipeline_status = client.get_pipeline_status(2310, 123)
```
### add statuses to pipeline
* doc -  https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#statuses-add
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| pipeline_id     |  int | - |
| statuses     |  list | - |
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
* doc -  https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#statuses-add
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| pipeline_id     |  int | - |
| status_id     |  int | - |
| name     |  str | - |
| sort     |  int | - |
| color     |  str | - |
```python
result = client.edit_pipeline_status(2310, 123, 'Новый Этап', sort=500, color="#fffeb2")
```
### delete status from pipeline
* doc -  https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#status-delete
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| pipeline_id     |  int | - |
| status_id     |  int | - |
```python

result = client.delete_status_from_pipeline(2310, 123)
```
### get contacts
* doc -  https://www.amocrm.ru/developers/content/crm_platform/contacts-api#contacts-list
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| limit     |  int  | 250 |
| page     |  int  | 1 |
| with_params     |  Optional[list]  | None |
| filters     |  Optional[dict]  | None |
| order     |  Optional[dict]  | None |
```python

contacts = client.get_contacts(limit=10, page=3, filters={'[updated_at][from]': '<timestamp>'})
```

### get contact
* doc -  https://www.amocrm.ru/developers/content/crm_platform/contacts-api#contact-detail
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| contact_id     |  int  | - |
```python

contact = client.get_contact(123989)
```
### create contacts
* doc -  https://www.amocrm.ru/developers/content/crm_platform/contacts-api#contacts-add
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| contacts     |  list  | - |
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
* doc -  https://www.amocrm.ru/developers/content/crm_platform/contacts-api#contacts-edit
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| contacts     |  list  | - |
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
### get companies
* doc -  https://www.amocrm.ru/developers/content/crm_platform/companies-api#companies-list
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| limit     |  int  | 250 |
| page     |  int  | 1 |
| with_params     |  Optional[list]  | None |
| filters     |  Optional[dict]  | None |
| order     |  Optional[dict]  | None |
```python

companies = client.get_companies(limit=10, page=3, filters={'[updated_at][from]': '<timestamp>'})
```
### get company
* doc -  https://www.amocrm.ru/developers/content/crm_platform/companies-api#company-detail
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| company_id     |  int  | - |
```python

company = client.get_company(9988)
```
### create companies
* doc -  https://www.amocrm.ru/developers/content/crm_platform/companies-api#companies-add
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| companies     |  list  | - |
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
* doc -  https://www.amocrm.ru/developers/content/crm_platform/companies-api#companies-edit
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| companies     |  list  | - |
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
### get catalogs
* doc -  https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#lists-list
* params:

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| page     |  int  | 1 |
| limit     |  int  | 250 |
```python
catalogs = client.get_catalogs(page=1, limit=5)
```
### get catalog
* doc -  https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#list-detail
* params: 
 
| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| catalog_id     |  int  | 1 |
```python
catalog = client.get_catalog(12319)
```
### create catalogs
* doc -  https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#lists-add
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| catalogs     |  list  | - |
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
* doc -  https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#lists-edit
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| catalogs     |  list  | - |
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
* doc -  https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#list-elements-list
* params: 
 
| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| catalogs_id     |  int  | - |
| page     |  int  | 1 |
| limit     |  int  | 250 |
| filters     |  Optional[dict]  | None |
```python
elements = client.get_catalog_elements(5787, page=3, limit=8)
```
### get element from catalog
* doc -  https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#list-elements-detail
* params:

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| catalogs_id     |  int  | - |
| element_id     |  int  | - |
```python
element = client.get_catalog_element(5787, 2301)
```
### add elements to catalog
* doc -  https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#list-elements-add
* params:

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| catalogs_id     |  int  | - |
| elements     |  list  | - |
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
* doc -  https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#list-elements-edit
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| catalogs_id     |  int  | - |
| elements     |  list  | - |
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
### get users
* doc -  https://www.amocrm.ru/developers/content/crm_platform/users-api#users-list
* params: 
 
| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| page     |  int  | 1 |
| limit     |  list  | 250 |
| with_role     |  bool  | False |
| with_group     |  bool  | False |
```python
users = client.get_users(page=1, limit=250)
```
### get user
* doc -  https://www.amocrm.ru/developers/content/crm_platform/users-api#user-detail
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| user_id     |  int  | 1 |
| with_role     |  bool  | False |
| with_group     |  bool  | False |
```python
user = client.get_user(2222, with_role=True, with_group=True)
```
### get webhooks
* doc -  https://www.amocrm.ru/developers/content/crm_platform/webhooks-api#webhooks-list
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| distansion     |  Optional[str]  | None |
```python
webhooks = client.get_webhooks()
```
### subscribe webhook
* doc -  https://www.amocrm.ru/developers/content/crm_platform/webhooks-api#webhook-subscribe
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| distansion     |  str  | - |
| settings     |  list  | - |
```python
result = client.subscribe_webhook(destination="https://example.test", settings=["add_lead"])
```
### get widgets
* doc -  https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widgets-list
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| page     |  int  | 1 |
| limit     |  int  | 250 |
```python
widgets = client.get_widgets(page=3, limit=22)
```
### get widget
* doc -  https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widget-detail
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| widget_code     |  str  | - |
```python
widget = client.get_widget('<widget_code>')
```
### install widget
* doc -  https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widget-install
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| widget_code     |  str  | - |
| **kwargs     |  str  | - |
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
* doc -  https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widget-uninstall
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| widget_code     |  str  | - |
```python
result = client.uninstall_widget('<widget_code>')
```
### get tasks
* doc -  https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-list
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| page     |  int  | 1 |
| limit     |  int  | 250 |
| filters     |  Optional[dict]  | None |
| order     |  Optional[dict]  | None |
```python
tasks = client.get_tasks(page=1, limit=10, filters={'[updated_at][from]': '<timestamp>'})
```
### get task
* doc -  https://www.amocrm.ru/developers/content/crm_platform/tasks-api#task-detail
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| task_id     |  int  | - |

```python
task = client.get_task(1288)
```
### add tasks
* doc -  https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-add
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| tasks     |  list  | - |

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
* doc -  https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-edit
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| tasks     |  list  | - |

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
* doc -  https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-complete
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| task_id     |  int  | - |
| is_completed |  bool  | - |
| result     |  str  | - |

```python
result = client.execution_task(1288, is_completed=True, result="Удалось связаться с клиентом")
```
### get tasks by entity type (leads|contacts|companies|customers)
* doc -  https://www.amocrm.ru/developers/content/crm_platform/tags-api#tags-list
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| entity_type     |  str  | - |
| page |  int  | 1 |
| limit     |  int  | 250 |
| filters     |  Optional[dict]  | None |

```python
tags = client.get_tags_by_entity_type('leads', page=1, limit=10)
```
### add tasks for entity type (leads|contacts|companies|customers)
* doc -  https://www.amocrm.ru/developers/content/crm_platform/tags-api#tags-add
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| entity_type     |  str  | - |
| tags |  list  | - |

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
### get custom fields
* doc - https://www.amocrm.ru/developers/content/crm_platform/custom-fields#common-info
```python
contacts_cf = client.get_contacts_custom_fields()
leads_cf = client.get_leads_custom_fields()
companies_cf = client.get_companies_custom_fields()
customers_cf = client.get_customers_custom_fields()
customer_segments_cf = client.get_customer_segments_custom_fields()
customer_segments_cf = client.get_customer_segments_custom_fields()
get_catalog_custom_fields = client.get_customer_segments_custom_fields('<catalog_id>')
```
### get custom field
* doc - https://www.amocrm.ru/developers/content/crm_platform/custom-fields#custom-field-detail
```python
contacts_cf = client.get_contacts_custom_field('<id>')
leads_cf = client.get_leads_custom_field('<id>')
companies_cf = client.get_companies_custom_field('<id>')
customers_cf = client.get_customers_custom_field('<id>')
customer_segments_cf = client.get_customer_segments_custom_field('<id>')
get_catalog_custom_fields = client.get_catalog_custom_field('<catalog_id>', '<id>')
```
### create custom field
* doc - https://www.amocrm.ru/developers/content/crm_platform/custom-fields#custom-fields-add
```python
contacts_cf = client.create_contacts_custom_field(['<cf>'])
leads_cf = client.create_leads_custom_field(['<cf>'])
companies_cf = client.create_companies_custom_field(['<cf>'])
customers_cf = client.create_customers_custom_field(['<cf>'])
customer_segments_cf = client.create_customer_segments_custom_field(['<cf>'])
get_catalog_custom_fields = client.create_catalog_custom_field('<catalog_id>', ['<cf>'])
```
### update custom field
* doc - https://www.amocrm.ru/developers/content/crm_platform/custom-fields#custom-fields-edit
```python
contacts_cf = client.update_contacts_custom_field(['<cf>'])
leads_cf = client.update_leads_custom_field(['<cf>'])
companies_cf = client.update_companies_custom_field(['<cf>'])
customers_cf = client.update_customers_custom_field(['<cf>'])
customer_segments_cf = client.update_customer_segments_custom_field(['<cf>'])
get_catalog_custom_fields = client.update_catalog_custom_field('<catalog_id>', ['<cf>'])
```