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
