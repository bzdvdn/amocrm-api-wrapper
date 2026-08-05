# wrapper for amocrm rest api

## Install

Install using `pip`...

    pip install amocrm-api-wrapper

## Async support

Every method has an async twin with the `_async` suffix (e.g. `get_leads_async`).
Async variants use `httpx.AsyncClient` natively and return awaitables:

```python
import asyncio
from amocrm_api import AmoOAuthClient

async def main():
    client = AmoOAuthClient('<access_token>', '<refresh_token>', '<crm_url>', '<client_id>', '<client_secret>', '<redirect_uri>')
    leads = await client.get_leads_async()
    print(leads)
    await client.close_async()

asyncio.run(main())
```

For the legacy client the async session is initialized lazily on the first
async call, no extra setup is required:

```python
import asyncio
from amocrm_api import AmoLegacyClient

async def main():
    client = AmoLegacyClient('<login>', '<token>', '<crm_url>')
    users = await client.get_users_async()
    print(users)

asyncio.run(main())
```

## Pagination

Methods that return collections across pages (`iter_*`) fetch all pages
lazily, so you don't have to manage `page`/`limit` manually. Sync variants
are generators, async variants are async generators:

```python
# sync
for lead in client.iter_leads(filters={"name": "x"}):
    print(lead["id"])

# async
async for contact in client.iter_contacts_async():
    print(contact["id"])
```

Available iterators:

| Method | Async twin | Notes |
| :--- | :--- | :--- |
| `iter_leads` | `iter_leads_async` | |
| `iter_contacts` | `iter_contacts_async` | |
| `iter_companies` | `iter_companies_async` | |
| `iter_tasks` | `iter_tasks_async` | |
| `iter_catalog_elements(catalog_id, ...)` | `iter_catalog_elements_async` | |
| `iter_tags_by_entity_type(entity_type, ...)` | `iter_tags_by_entity_type_async` | |

All accept the same filters/order/with-params as the corresponding `get_*`
methods, but the `page` argument is handled for you.

## Usage

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

## Documentation

Per-entity API reference is split into `docs/`. Every method has an async
twin with the `_async` suffix; each file ends with an async usage example:

| Entity | File |
| :--- | :--- |
| Account | [docs/account.md](docs/account.md) |
| Leads | [docs/leads.md](docs/leads.md) |
| Unsorted leads | [docs/unsorted.md](docs/unsorted.md) |
| Pipelines | [docs/pipelines.md](docs/pipelines.md) |
| Contacts | [docs/contacts.md](docs/contacts.md) |
| Companies | [docs/companies.md](docs/companies.md) |
| Catalogs | [docs/catalogs.md](docs/catalogs.md) |
| Tasks | [docs/tasks.md](docs/tasks.md) |
| Users | [docs/users.md](docs/users.md) |
| Webhooks | [docs/webhooks.md](docs/webhooks.md) |
| Widgets | [docs/widgets.md](docs/widgets.md) |
| Custom fields | [docs/custom_fields.md](docs/custom_fields.md) |

See [CHANGELOG.md](CHANGELOG.md) for release history.