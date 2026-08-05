### get custom fields

- doc - https://www.amocrm.ru/developers/content/crm_platform/custom-fields#common-info

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

- doc - https://www.amocrm.ru/developers/content/crm_platform/custom-fields#custom-field-detail

```python
contacts_cf = client.get_contacts_custom_field('<id>')
leads_cf = client.get_leads_custom_field('<id>')
companies_cf = client.get_companies_custom_field('<id>')
customers_cf = client.get_customers_custom_field('<id>')
customer_segments_cf = client.get_customer_segments_custom_field('<id>')
get_catalog_custom_fields = client.get_catalog_custom_field('<catalog_id>', '<id>')
```

### create custom field

- doc - https://www.amocrm.ru/developers/content/crm_platform/custom-fields#custom-fields-add

```python
contacts_cf = client.create_contacts_custom_field(['<cf>'])
leads_cf = client.create_leads_custom_field(['<cf>'])
companies_cf = client.create_companies_custom_field(['<cf>'])
customers_cf = client.create_customers_custom_field(['<cf>'])
customer_segments_cf = client.create_customer_segments_custom_field(['<cf>'])
get_catalog_custom_fields = client.create_catalog_custom_field('<catalog_id>', ['<cf>'])
```

### update custom field

- doc - https://www.amocrm.ru/developers/content/crm_platform/custom-fields#custom-fields-edit

```python
contacts_cf = client.update_contacts_custom_field(['<cf>'])
leads_cf = client.update_leads_custom_field(['<cf>'])
companies_cf = client.update_companies_custom_field(['<cf>'])
customers_cf = client.update_customers_custom_field(['<cf>'])
customer_segments_cf = client.update_customer_segments_custom_field(['<cf>'])
get_catalog_custom_fields = client.update_catalog_custom_field('<catalog_id>', ['<cf>'])
```

---

## Async

Every method above has an async twin with the `_async` suffix
(e.g. `get_*_async`, `create_*_async`) that uses `httpx.AsyncClient` natively
and returns an awaitable. Example:

```python
import asyncio

async def main():
    leads_cf = await client.get_leads_custom_fields_async()
    await client.close_async()

asyncio.run(main())
```
