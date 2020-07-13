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
headers = {
    "IF-MODIFIED-SINCE": f"{date_time}",
    "Content-Type": "application/json",
}

client.update_session_params(headers)
```
## account info
=======
----------------------------------------------
* doc - https://www.amocrm.ru/developers/content/api/account
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| with_custom_fields     |  bool  | false |
| with_users    | bool |   false |
| with_pipelines    | bool |   false |
| with_groups    | bool |   false |
| with_note_types    | bool |   false |
| with_task_types    | bool |   false |
```python
accounts = client.get_account_info(with_custom_fields=True)
```
## create or update leads
----------------------------------------------
* doc - https://www.amocrm.ru/developers/content/api/leads
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| add     |  list  | None |
| update    | list |  None |
```python
add = [{
    "name": "Покупка карандашей",
    "created_at": "1508101200",
    "updated_at": "1508274000",
    "status_id": "13670637",
    "responsible_user_id": "957083",
    "sale": "5000",
    "tags": "pencil, buy",
    "contacts_id": [
        "1099149"
    ],
    "company_id": "1099148",
    "catalog_elements_id": {
        99999: {
            111111: 10
        }
    }}]
update = [{
    "id": "1090256",
    "updated_at": "1508360400",
    "sale": "10000",
}]
result = client.create_or_update_leads(add=add, update=update)
```
## get leads
----------------------------------------------
* doc - https://www.amocrm.ru/developers/content/api/leads
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| limit_rows     |  int  | 500 |
| limit_offset    | int |  0 |
| id    | Union[list, int, None]  |  None |
| query    | Optional[str]  |  None |
| status    | Optional[str]  |  None |
| responsible_user_id | Union[list, int, None]  |  None |
| with_params    | Optional[list]  |  None |


```python
leads = client.get_leads(limit_rows=20, limit_offset=50)
```

## create or update contacts
----------------------------------------------
* doc - https://www.amocrm.ru/developers/content/api/contacts
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| add     |  list  | None |
| update    | list |  None |
```python
add = [{
    	"name": "Александр Крылов",
		"responsible_user_id": "504141",
		"created_by": "504141",
		"created_at": "1509051600",
		"tags": "важный,доставка",
		"leads_id": [
			"45615",
			"43510"
		],
		"company_id": "30615",}]
update = [{
    "id": "41560",
    "updated_at": "1508965200",
    "custom_fields": [{
        "id": "4396819",
        "values": [{
            "value": "example@example.moc",
            "enum": "WORK"
        }]
    }]
}]
result = client.create_or_update_contacts(add=add, update=update)
```
## get contacts
----------------------------------------------
* doc - https://www.amocrm.ru/developers/content/api/contacts
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| limit_rows     |  int  | 500 |
| limit_offset    | int |  0 |
| id    | Union[list, int, None]  |  None |
| query    | Optional[str]  |  None |
| status    | Optional[str]  |  None |
| responsible_user_id | Union[list, int, None]  |  None |
| with_params    | Optional[list]  |  None |

```python
contacts = client.get_contacts(limit_rows=20, limit_offset=50)
```

## create or update companies
----------------------------------------------
* doc - https://www.amocrm.ru/developers/content/api/companies
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| add     |  list  | None |
| update    | list |  None |
```python
add = [{
    "name": "ООО Компания",
    "responsible_user_id": "504141",
    "created_by": "504141",
    "created_at": "1509051600",
    "tags": "недвижимость,застройка,аренда",
    "leads_id": [
        "45615",
        "43510"
    ],}]
update = [{
    "id": "41389",
    "updated_at": "1508965200",
    "custom_fields": [{
        "id": "315289",
        "values": [{
            "value": "example.moc",
            "enum": "WEB"
        }]
    }]
}]
result = client.create_or_update_companies(add=add, update=update)
```
## get companies
----------------------------------------------
* doc - https://www.amocrm.ru/developers/content/api/companies
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| limit_rows     |  int  | 500 |
| limit_offset    | int |  0 |
| id    | Union[list, int, None]  |  None |
| query    | Optional[str]  |  None |
| status    | Optional[str]  |  None |
| responsible_user_id | Union[list, int, None]  |  None |
| with_params    | Optional[list]  |  None |

```python
companies = client.get_companies(limit_rows=20, limit_offset=50)
```

## create or update customers
----------------------------------------------
* doc - https://www.amocrm.ru/developers/content/api/customers
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| add     |  list  | None |
| update    | list |  None |
```python
add = [{
    "name": "ООО СпецГорСтрой",
    "next_date": "1508878800",
    "created_at": "1508533200",
    "responsible_user_id": "504141",
    "created_by": "504141",
    "next_price": "5000",
    "periodicity": "7",
    "tags": "продажи, маркеры",
    "period_id": "15489654",
    "contacts_id": [
        "496531"
    ],
    "company_id": "475621"}]
update = [{
    "id": "466791",
    "updated_at": "1508619600",
    "next_date": "1508878800",
    "next_price": "1508706000",
    "custom_fields": [{
        "id": "4400021",
        "values": [
            "3692471",
            "3692472",
            "3692473"
        ]
    }]
}]
result = client.create_or_update_companies(add=add, update=update)
```
## get customers
----------------------------------------------
* doc - https://www.amocrm.ru/developers/content/api/customers
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| limit_rows     |  int  | 500 |
| limit_offset    | int |  0 |
| id    | Union[list, int, None]  |  None |
| query    | Optional[str]  |  None |
| status    | Optional[str]  |  None |
| responsible_user_id | Union[list, int, None]  |  None |
| with_params    | Optional[list]  |  None |

```python
customers = client.get_customers(limit_rows=20, limit_offset=50)
```
## delete customers
* doc - https://www.amocrm.ru/developers/content/api/customers
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| delete_ids     |  list  | required |
```python
delete_ids = ['123', '1234', '12345']
result = client.delete_customers(delete_ids)
```
## create or update customers
----------------------------------------------
* doc - https://www.amocrm.ru/developers/content/api/customers
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| add     |  list  | None |
| update    | list |  None |
```python
add = [{
    "name": "ООО СпецГорСтрой",
    "next_date": "1508878800",
    "created_at": "1508533200",
    "responsible_user_id": "504141",
    "created_by": "504141",
    "next_price": "5000",
    "periodicity": "7",
    "tags": "продажи, маркеры",
    "period_id": "15489654",
    "contacts_id": [
        "496531"
    ],
    "company_id": "475621"}]
update = [{
    "id": "466791",
    "updated_at": "1508619600",
    "next_date": "1508878800",
    "next_price": "1508706000",
    "custom_fields": [{
        "id": "4400021",
        "values": [
            "3692471",
            "3692472",
            "3692473"
        ]
    }]
}]
result = client.create_or_update_companies(add=add, update=update)
```
## get customers
----------------------------------------------
* doc - https://www.amocrm.ru/developers/content/api/customers
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| limit_rows     |  int  | 500 |
| limit_offset    | int |  0 |
| id    | Union[list, int, None]  |  None |
| query    | Optional[str]  |  None |
| status    | Optional[str]  |  None |
| responsible_user_id | Union[list, int, None]  |  None |
| with_params    | Optional[list]  |  None |

```python
customers = client.get_customers(limit_rows=20, limit_offset=50)
```
## delete customers
* doc - https://www.amocrm.ru/developers/content/api/customers
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| delete_ids     |  list  | required |
```python
delete_ids = ['123', '1234', '12345']
result = client.delete_customers(delete_ids)
```

## create transactions
* doc - https://www.amocrm.ru/developers/content/api/customers
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| add     |  list  | required |
```python
add = [{
    "customer_id": "466791",
    "date": "1507582800",
    "price": "15000",
    "comment": "Всё прошло успешно",
    "next_date": "1508878800",
    "next_price": "20000",
    "elements": {
        9999: {
            111111: 3
        }
    }
}]
result = client.create_transactions(add=add)
```
## comment transactions
* doc - https://www.amocrm.ru/developers/content/api/customers
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| update     |  list  | required |
```python
update = [{
    "transaction_id": "5396",
    "comment": "Составить договор"
}]
result = client.delete_transactions(update)
```
## get transactions
* doc - https://www.amocrm.ru/developers/content/api/customers
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| limit_rows     |  int  | 500 |
| limit_offset     |  int  | 0 |
| id     |  Optional[int]  | None |
| customer_id     |  Optional[int]  | None |
```python
transactions = client.get_transactions()
```
## update customers periods
* doc - https://www.amocrm.ru/developers/content/api/customers
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| update     |  list  | required |
```python
update = [{
    "period": "5",
    "id": "15563",
    "color": "#000000",
    "sort": "1"
}]
result = client.update_customer_periods(update)
```
## get customers periods
* doc - https://www.amocrm.ru/developers/content/api/customers

```python
periods = client.get_customer_periods()
```

## get tasks
----------------------------------------------
* doc -  https://www.amocrm.ru/developers/content/api/tasks
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| limit_rows     |  int  | 500 |
| limit_offset    | int |  0 |
| id    | Union[list, int, None]  |  None |
| element_id    | Optional[str]  |  None |
| type    | Optional[str]  |  None |
| responsible_user_id | Union[list, int, None]  |  None |

```python
tasks = client.get_tasks(limit_rows=20, limit_offset=50)
```
## create tasks
* doc - https://www.amocrm.ru/developers/content/api/tasks
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| add     |  Optional[list]  | None |
| update     |  Optional[list]  | None |
```python
add = [{
    "element_id": "496537",
    "element_type": "1",
    "complete_till_at": "1508706000",
    "task_type": "1",
    "text": "Не забыть перезвонить",
    "created_at": "1508706000",
    "updated_at": "1508706000",
    "responsible_user_id": "504141",
    "created_by": "504141"
}]
result = client.create_tasks(add=add)
```
## get notes
----------------------------------------------
* doc -  https://www.amocrm.ru/developers/content/api/notes
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| limit_rows     |  int  | 500 |
| limit_offset    | int |  0 |
| id    | Union[list, int, None]  |  None |
| element_id    | Optional[str]  |  None |
| note_type    | Optional[str]  |  None |
| if_modified_since | Optional[str]  |  None |

```python
notes = client.get_notes(limit_rows=20, limit_offset=50)
```
## create or update notes
* doc - https://www.amocrm.ru/developers/content/api/notes
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| add     |  Optional[list]  | None |
| update     |  Optional[list]  | None |
```python
add = [{
    "element_id": "1099238",
    "element_type": "1",
    "text": "Примечание",
    "note_type": "4",
    "created_at": "1509570000",
    "responsible_user_id": "504141",
    "created_by": "504141"
}]
update = [{
    "id": "3323256",
    "updated_at": "1509656400",
    "text": "Изменение примечания"
}]
result = client.create_or_update_notes(add=add, update=update)
```
## create incoming leads by sip
* doc - https://www.amocrm.ru/developers/content/api/unsorted
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| add     |  Optional[list]  | None |
```python
add = [{
    "<data>"
}]
result = client.create_sip_incoming_leads(add=add)
```

## create incoming leads by form
* doc - https://www.amocrm.ru/developers/content/api/unsorted
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| add     |  Optional[list]  | None |
```python
add = [{
    "<data>"
}]
result = client.create_form_incoming_leads(add=add)
```
## accept incoming leads
* doc - https://www.amocrm.ru/developers/content/api/unsorted
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| accept     |  list  | required |
| user_id     |  int  | required |
| status_id     |  int  | required |
```python
result = client.accept_incoming_leads(accept=['123', '1234', '444'], user_id=1, status_id=2310)
```
## decline incoming leads
* doc - https://www.amocrm.ru/developers/content/api/unsorted
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| decline     |  list  | required |
| user_id     |  int  | required |
```python
result = client.accept_incoming_leads(decline=['123', '1234', '444'], user_id=1)
```
## get incomings leads
* doc - https://www.amocrm.ru/developers/content/api/unsorted
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| page     |  int  | 1 |
| page_size     |  int  | 500 |
| categories     |  Optional[list]  | None |
| pipeline_id     |  Optional[list]  | None |
| order_by     |  str  | 'asc' |
```python
result = client.get_incoming_leads()
```
## get incomings leads summary
* doc - https://www.amocrm.ru/developers/content/api/unsorted
* params:  

| name       | type                | default value |
| :------------------:|:------------------:| :------------------:|
| date_from     |  str  | required |
| date_to     |  str  | required |
```python
result = client.get_incoming_leads_summary(date_from, date_to)
```