# wrapper for amocrm rest api

## Install
Install using `pip`...

    pip install amocrm-api-wrapper


## Usage
=======
```python
from amocrm import AmocrmLegacyClient # for login password auth
from amocrm import AmocrmOAuthClient # for oauth
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
=======
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
=======
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
| responsible_user_id    | Union[list, int, None]  |  None |
| with_params    | Optional[list]  |  None |


```python
leads = client.get_leads(limit_rows=20, limit_offset=50)
```