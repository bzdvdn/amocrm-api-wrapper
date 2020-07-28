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

client = AmocrmLegacyClient('<login>', '<password>', '<crm_url>')
client = AmocrmOAuthClient('<access_token>', '<refresh_token>', '<crm_url>', '<client_id>', '<client_secret>', '<redirect_uri>')
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
|
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
statuses = [
    {
        "name": "Новый этап",
        "sort": 100,
        "color": "#fffeb2"
    },
]
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