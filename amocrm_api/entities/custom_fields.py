
from urllib.parse import urlencode

from .base import Entity


class CustomFields(Entity):
    def _build_get_custom_fields_url(
        self,
        entity: str,
        page: int | None,
        limit: int | None = None,
        field_type: str | None = None,
        order: dict | None = None,
    ) -> str:
        url = f"{self.crm_url}/api/v4/{entity}/custom_fields"
        params: dict = {}
        if page:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if field_type:
            params["filter[type][0]"] = field_type
        if order:
            order_query = {f"order[{k}]": v for k, v in order.items()}
            params.update(order_query)
        if params:
            url = f"{url}?{urlencode(params)}"
        return url

    def _get_custom_fields(
        self,
        entity: str,
        page: int | None = None,
        limit: int | None = None,
        field_type: str | None = None,
        order: dict | None = None,
    ) -> dict:
        url = self._build_get_custom_fields_url(entity, page, limit, field_type, order)
        return self._send_api_request("get", url)

    def get_contacts_custom_fields(
        self,
        page: int | None = None,
        limit: int | None = None,
        field_type: str | None = None,
        order: dict | None = None,
    ) -> dict:
        return self._get_custom_fields(
            "contacts", page=page, limit=limit, field_type=field_type, order=order
        )

    def get_leads_custom_fields(
        self,
        page: int | None = None,
        limit: int | None = None,
        field_type: str | None = None,
        order: dict | None = None,
    ) -> dict:
        return self._get_custom_fields(
            "leads", page=page, limit=limit, field_type=field_type, order=order
        )

    def get_companies_custom_fields(
        self,
        page: int | None = None,
        limit: int | None = None,
        field_type: str | None = None,
        order: dict | None = None,
    ) -> dict:
        return self._get_custom_fields(
            "companies", page=page, limit=limit, field_type=field_type, order=order
        )

    def get_customers_custom_fields(
        self,
        page: int | None = None,
        limit: int | None = None,
        field_type: str | None = None,
        order: dict | None = None,
    ) -> dict:
        return self._get_custom_fields(
            "customers", page=page, limit=limit, field_type=field_type, order=order
        )

    def get_customer_segments_custom_fields(
        self,
        page: int | None = None,
        limit: int | None = None,
        field_type: str | None = None,
        order: dict | None = None,
    ) -> dict:
        return self._get_custom_fields(
            "customers/segments",
            page=page,
            limit=limit,
            field_type=field_type,
            order=order,
        )

    def get_catalog_custom_fields(
        self,
        catalog_id: int,
        page: int | None = None,
        limit: int | None = None,
        field_type: str | None = None,
        order: dict | None = None,
    ) -> dict:
        return self._get_custom_fields(
            f"catalogs/{catalog_id}",
            page=page,
            limit=limit,
            field_type=field_type,
            order=order,
        )

    def _get_custom_field_by_entity_type(
        self, entity_type: str, custom_field_id: int
    ) -> dict:
        """Get custom field
    
        Args:
            entity_type (str): entity type
            custom_field_id (int): id of custom field
    
        Returns:
            dict: {
                "id": 3,
                "name": "Телефон",
                "type": "multitext",
                "account_id": 28805383,
                "code": "PHONE",
                "sort": 4,
                "is_api_only": false,
                "enums": [
                    {
                        "id": 1,
                        "value": "WORK",
                        "sort": 2
                    },
                    {
                        "id": 3,
                        "value": "WORKDD",
                        "sort": 4
                    },
                    {
                        "id": 5,
                        "value": "MOB",
                        "sort": 6
                    },
                    {
                        "id": 7,
                        "value": "FAX",
                        "sort": 8
                    },
                    {
                        "id": 9,
                        "value": "HOME",
                        "sort": 10
                    },
                    {
                        "id": 11,
                        "value": "OTHER",
                        "sort": 12
                    }
                ],
                "group_id": null,
                "required_statuses": [],
                "is_deletable": false,
                "is_predefined": true,
                "entity_type": "contacts",
                "remind": null,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/contacts/custom_fields/3"
                    }
                }
            }
        """
        url = f"{self.crm_url}/api/v4/{entity_type}/custom_fields/{custom_field_id}"
        return self._send_api_request("get", url)

    def get_leads_custom_field(self, custom_field_id: int) -> dict:
        return self._get_custom_field_by_entity_type("leads", custom_field_id)

    def get_contacts_custom_field(self, custom_field_id: int) -> dict:
        return self._get_custom_field_by_entity_type("contacts", custom_field_id)

    def get_companies_custom_field(self, custom_field_id: int) -> dict:
        return self._get_custom_field_by_entity_type("companies", custom_field_id)

    def get_customers_custom_field(self, custom_field_id: int) -> dict:
        return self._get_custom_field_by_entity_type("customers", custom_field_id)

    def get_customers_segments_custom_field(self, custom_field_id: int) -> dict:
        return self._get_custom_field_by_entity_type(
            "customers/segments", custom_field_id
        )

    def get_catalog_custom_field(self, catalog_id: int, custom_field_id: int) -> dict:
        return self._get_custom_field_by_entity_type(
            f"catalogs/{catalog_id}", custom_field_id
        )

    def _create_custom_fields(self, entity_type: str, custom_fields: list) -> dict:
        """Create custom fields by entity type
        Doc: https://www.amocrm.ru/developers/content/crm_platform/custom-fields#custom-fields-add
        Args:
            entity_type (str): entity type
            custom_fields (list): list
    
        Returns:
            dict: {
            "_total_items": 1,
            "_embedded": {
                "custom_fields": [
                    {
                        "name": "multi select",
                        "type": "multiselect",
                        "sort": 510,
                        "settings": null,
                        "is_predefined": false,
                        "id": 4457223,
                        "remind": null,
                        "is_api_only": false,
                        "enums": [
                            {
                                "value": "Значение 1",
                                "sort": 1,
                                "id": 3778801
                            },
                            {
                                "value": "Значение 2",
                                "sort": 2,
                                "id": 3778803
                            }
                        ],
                        "group_id": null,
                        "required_statuses": [
                            {
                                "status_id": 20540473,
                                "pipeline_id": 16056
                            },
                        ],
                        "_links": {
                            "self": {
                                "href": "https://example.amocrm.ru/api/v4/custom_fields/4457223/"
                            }
                        }
                    }
                ]
            }
        }
        """
        url = f"{self.crm_url}/api/v4/{entity_type}/custom_fields"
        return self._send_api_request("post", url, custom_fields)

    def create_leads_custom_fields(self, custom_fields: list) -> dict:
        return self._create_custom_fields("leads", custom_fields)

    def create_contacts_custom_fields(self, custom_fields: list) -> dict:
        return self._create_custom_fields("contacts", custom_fields)

    def create_companies_custom_fields(self, custom_fields: list) -> dict:
        return self._create_custom_fields("companies", custom_fields)

    def create_customers_custom_fields(self, custom_fields: list) -> dict:
        return self._create_custom_fields("customers", custom_fields)

    def create_customers_segments_custom_fields(self, custom_fields: list) -> dict:
        return self._create_custom_fields("customers/segments", custom_fields)

    def create_catalog_custom_fields(
        self, catalog_id: int, custom_fields: list
    ) -> dict:
        return self._create_custom_fields(f"catalogs/{catalog_id}", custom_fields)

    def _update_custom_fields(self, entity_type: str, custom_fields: list) -> dict:
        """Create custom fields by entity type
        Doc: https://www.amocrm.ru/developers/content/crm_platform/custom-fields#custom-fields-add
        Args:
            entity_type (str): entity type
            custom_fields (list): list
    
        Returns:
            dict: {
            "_total_items": 1,
            "_embedded": {
                "custom_fields": [
                    {
                        "name": "multi select",
                        "type": "multiselect",
                        "sort": 510,
                        "settings": null,
                        "is_predefined": false,
                        "id": 4457223,
                        "remind": null,
                        "is_api_only": false,
                        "enums": [
                            {
                                "value": "Значение 1",
                                "sort": 1,
                                "id": 3778801
                            },
                            {
                                "value": "Значение 2",
                                "sort": 2,
                                "id": 3778803
                            }
                        ],
                        "group_id": null,
                        "required_statuses": [
                            {
                                "status_id": 20540473,
                                "pipeline_id": 16056
                            },
                        ],
                        "_links": {
                            "self": {
                                "href": "https://example.amocrm.ru/api/v4/custom_fields/4457223/"
                            }
                        }
                    }
                ]
            }
        }
        """
        url = f"{self.crm_url}/api/v4/{entity_type}/custom_fields"
        return self._send_api_request("patch", url, custom_fields)

    async def _get_custom_fields_async(
        self,
        entity: str,
        page: int | None = None,
        limit: int | None = None,
        field_type: str | None = None,
        order: dict | None = None,
    ) -> dict:
        """Async version of _get_custom_fields."""
        url = self._build_get_custom_fields_url(entity, page, limit, field_type, order)
        return await self._send_api_request_async("get", url)

    async def get_contacts_custom_fields_async(
        self,
        page: int | None = None,
        limit: int | None = None,
        field_type: str | None = None,
        order: dict | None = None,
    ) -> dict:
        return await self._get_custom_fields_async(
            "contacts", page=page, limit=limit, field_type=field_type, order=order
        )

    async def get_leads_custom_fields_async(
        self,
        page: int | None = None,
        limit: int | None = None,
        field_type: str | None = None,
        order: dict | None = None,
    ) -> dict:
        return await self._get_custom_fields_async(
            "leads", page=page, limit=limit, field_type=field_type, order=order
        )

    async def get_companies_custom_fields_async(
        self,
        page: int | None = None,
        limit: int | None = None,
        field_type: str | None = None,
        order: dict | None = None,
    ) -> dict:
        return await self._get_custom_fields_async(
            "companies", page=page, limit=limit, field_type=field_type, order=order
        )

    async def get_customers_custom_fields_async(
        self,
        page: int | None = None,
        limit: int | None = None,
        field_type: str | None = None,
        order: dict | None = None,
    ) -> dict:
        return await self._get_custom_fields_async(
            "customers", page=page, limit=limit, field_type=field_type, order=order
        )

    async def get_customer_segments_custom_fields_async(
        self,
        page: int | None = None,
        limit: int | None = None,
        field_type: str | None = None,
        order: dict | None = None,
    ) -> dict:
        return await self._get_custom_fields_async(
            "customers/segments",
            page=page,
            limit=limit,
            field_type=field_type,
            order=order,
        )

    async def get_catalog_custom_fields_async(
        self,
        catalog_id: int,
        page: int | None = None,
        limit: int | None = None,
        field_type: str | None = None,
        order: dict | None = None,
    ) -> dict:
        return await self._get_custom_fields_async(
            f"catalogs/{catalog_id}",
            page=page,
            limit=limit,
            field_type=field_type,
            order=order,
        )

    async def _get_custom_field_by_entity_type_async(
        self, entity_type: str, custom_field_id: int
    ) -> dict:
        """Async version of _get_custom_field_by_entity_type."""
        url = f"{self.crm_url}/api/v4/{entity_type}/custom_fields/{custom_field_id}"
        return await self._send_api_request_async("get", url)

    async def get_leads_custom_field_async(self, custom_field_id: int) -> dict:
        return await self._get_custom_field_by_entity_type_async(
            "leads", custom_field_id
        )

    async def get_contacts_custom_field_async(self, custom_field_id: int) -> dict:
        return await self._get_custom_field_by_entity_type_async(
            "contacts", custom_field_id
        )

    async def get_companies_custom_field_async(self, custom_field_id: int) -> dict:
        return await self._get_custom_field_by_entity_type_async(
            "companies", custom_field_id
        )

    async def get_customers_custom_field_async(self, custom_field_id: int) -> dict:
        return await self._get_custom_field_by_entity_type_async(
            "customers", custom_field_id
        )

    async def get_customers_segments_custom_field_async(
        self, custom_field_id: int
    ) -> dict:
        return await self._get_custom_field_by_entity_type_async(
            "customers/segments", custom_field_id
        )

    async def get_catalog_custom_field_async(
        self, catalog_id: int, custom_field_id: int
    ) -> dict:
        return await self._get_custom_field_by_entity_type_async(
            f"catalogs/{catalog_id}", custom_field_id
        )

    async def _create_custom_fields_async(
        self, entity_type: str, custom_fields: list
    ) -> dict:
        """Async version of _create_custom_fields."""
        url = f"{self.crm_url}/api/v4/{entity_type}/custom_fields"
        return await self._send_api_request_async("post", url, custom_fields)

    async def create_leads_custom_fields_async(self, custom_fields: list) -> dict:
        return await self._create_custom_fields_async("leads", custom_fields)

    async def create_contacts_custom_fields_async(self, custom_fields: list) -> dict:
        return await self._create_custom_fields_async("contacts", custom_fields)

    async def create_companies_custom_fields_async(self, custom_fields: list) -> dict:
        return await self._create_custom_fields_async("companies", custom_fields)

    async def create_customers_custom_fields_async(self, custom_fields: list) -> dict:
        return await self._create_custom_fields_async("customers", custom_fields)

    async def create_customers_segments_custom_fields_async(
        self, custom_fields: list
    ) -> dict:
        return await self._create_custom_fields_async(
            "customers/segments", custom_fields
        )

    async def create_catalog_custom_fields_async(
        self, catalog_id: int, custom_fields: list
    ) -> dict:
        return await self._create_custom_fields_async(
            f"catalogs/{catalog_id}", custom_fields
        )

    async def _update_custom_fields_async(
        self, entity_type: str, custom_fields: list
    ) -> dict:
        """Async version of _update_custom_fields."""
        url = f"{self.crm_url}/api/v4/{entity_type}/custom_fields"
        return await self._send_api_request_async("patch", url, custom_fields)

    async def update_leads_custom_fields_async(self, custom_fields: list) -> dict:
        return await self._update_custom_fields_async("leads", custom_fields)

    async def update_contacts_custom_fields_async(self, custom_fields: list) -> dict:
        return await self._update_custom_fields_async("contacts", custom_fields)

    async def update_companies_custom_fields_async(self, custom_fields: list) -> dict:
        return await self._update_custom_fields_async("companies", custom_fields)

    async def update_customers_custom_fields_async(self, custom_fields: list) -> dict:
        return await self._update_custom_fields_async("customers", custom_fields)

    async def update_customers_segments_custom_fields_async(
        self, custom_fields: list
    ) -> dict:
        return await self._update_custom_fields_async(
            "customers/segments", custom_fields
        )

    async def update_catalog_custom_fields_async(
        self, catalog_id: int, custom_fields: list
    ) -> dict:
        return await self._update_custom_fields_async(
            f"catalogs/{catalog_id}", custom_fields
        )

    def update_leads_custom_fields(self, custom_fields: list) -> dict:
        return self._update_custom_fields("leads", custom_fields)

    def update_contacts_custom_fields(self, custom_fields: list) -> dict:
        return self._update_custom_fields("contacts", custom_fields)

    def update_companies_custom_fields(self, custom_fields: list) -> dict:
        return self._update_custom_fields("companies", custom_fields)

    def update_customers_custom_fields(self, custom_fields: list) -> dict:
        return self._update_custom_fields("customers", custom_fields)

    def update_customers_segments_custom_fields(self, custom_fields: list) -> dict:
        return self._update_custom_fields("customers/segments", custom_fields)

    def update_catalog_custom_fields(
        self, catalog_id: int, custom_fields: list
    ) -> dict:
        return self._update_custom_fields(f"catalogs/{catalog_id}", custom_fields)

    def _delete_custom_field(
        self, entity_type: str, custom_field_id: int
    ) -> dict:
        """Delete custom field by id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/custom-fields#custom-fields-delete
        """
        url = f"{self.crm_url}/api/v4/{entity_type}/custom_fields/{custom_field_id}"
        return self._send_api_request("delete", url)

    def delete_leads_custom_field(self, custom_field_id: int) -> dict:
        return self._delete_custom_field("leads", custom_field_id)

    def delete_contacts_custom_field(self, custom_field_id: int) -> dict:
        return self._delete_custom_field("contacts", custom_field_id)

    def delete_companies_custom_field(self, custom_field_id: int) -> dict:
        return self._delete_custom_field("companies", custom_field_id)

    def delete_customers_custom_field(self, custom_field_id: int) -> dict:
        return self._delete_custom_field("customers", custom_field_id)

    def delete_catalog_custom_field(
        self, catalog_id: int, custom_field_id: int
    ) -> dict:
        return self._delete_custom_field(
            f"catalogs/{catalog_id}", custom_field_id
        )

    def delete_customers_segments_custom_field(
        self, custom_field_id: int
    ) -> dict:
        return self._delete_custom_field(
            "customers/segments", custom_field_id
        )

    async def _delete_custom_field_async(
        self, entity_type: str, custom_field_id: int
    ) -> dict:
        """Async version of _delete_custom_field."""
        url = f"{self.crm_url}/api/v4/{entity_type}/custom_fields/{custom_field_id}"
        return await self._send_api_request_async("delete", url)

    async def delete_leads_custom_field_async(self, custom_field_id: int) -> dict:
        return await self._delete_custom_field_async("leads", custom_field_id)

    async def delete_contacts_custom_field_async(self, custom_field_id: int) -> dict:
        return await self._delete_custom_field_async("contacts", custom_field_id)

    async def delete_companies_custom_field_async(self, custom_field_id: int) -> dict:
        return await self._delete_custom_field_async("companies", custom_field_id)

    async def delete_customers_custom_field_async(self, custom_field_id: int) -> dict:
        return await self._delete_custom_field_async("customers", custom_field_id)

    async def delete_catalog_custom_field_async(
        self, catalog_id: int, custom_field_id: int
    ) -> dict:
        return await self._delete_custom_field_async(
            f"catalogs/{catalog_id}", custom_field_id
        )

    async def delete_customers_segments_custom_field_async(
        self, custom_field_id: int
    ) -> dict:
        return await self._delete_custom_field_async(
            "customers/segments", custom_field_id
        )

    def _get_custom_field_groups(
        self, entity_type: str, group_id: str | None = None
    ) -> dict:
        """Get custom field groups
        Doc: https://www.amocrm.ru/developers/content/crm_platform/custom-fields#custom-field-groups
        """
        url = f"{self.crm_url}/api/v4/{entity_type}/custom_fields/groups"
        if group_id is not None:
            url = f"{url}/{group_id}"
        return self._send_api_request("get", url)

    def get_leads_custom_field_groups(
        self, group_id: str | None = None
    ) -> dict:
        return self._get_custom_field_groups("leads", group_id)

    def get_contacts_custom_field_groups(
        self, group_id: str | None = None
    ) -> dict:
        return self._get_custom_field_groups("contacts", group_id)

    def get_companies_custom_field_groups(
        self, group_id: str | None = None
    ) -> dict:
        return self._get_custom_field_groups("companies", group_id)

    def get_customers_custom_field_groups(
        self, group_id: str | None = None
    ) -> dict:
        return self._get_custom_field_groups("customers", group_id)

    async def _get_custom_field_groups_async(
        self, entity_type: str, group_id: str | None = None
    ) -> dict:
        """Async version of _get_custom_field_groups."""
        url = f"{self.crm_url}/api/v4/{entity_type}/custom_fields/groups"
        if group_id is not None:
            url = f"{url}/{group_id}"
        return await self._send_api_request_async("get", url)

    async def get_leads_custom_field_groups_async(
        self, group_id: str | None = None
    ) -> dict:
        return await self._get_custom_field_groups_async("leads", group_id)

    async def get_contacts_custom_field_groups_async(
        self, group_id: str | None = None
    ) -> dict:
        return await self._get_custom_field_groups_async("contacts", group_id)

    async def get_companies_custom_field_groups_async(
        self, group_id: str | None = None
    ) -> dict:
        return await self._get_custom_field_groups_async("companies", group_id)

    async def get_customers_custom_field_groups_async(
        self, group_id: str | None = None
    ) -> dict:
        return await self._get_custom_field_groups_async("customers", group_id)

    def _create_custom_field_groups(
        self, entity_type: str, groups: list
    ) -> dict:
        """Create custom field groups
        Doc: https://www.amocrm.ru/developers/content/crm_platform/custom-fields#custom-field-groups
        """
        url = f"{self.crm_url}/api/v4/{entity_type}/custom_fields/groups"
        return self._send_api_request("post", url, groups)

    def create_leads_custom_field_groups(self, groups: list) -> dict:
        return self._create_custom_field_groups("leads", groups)

    def create_contacts_custom_field_groups(self, groups: list) -> dict:
        return self._create_custom_field_groups("contacts", groups)

    def create_companies_custom_field_groups(self, groups: list) -> dict:
        return self._create_custom_field_groups("companies", groups)

    def create_customers_custom_field_groups(self, groups: list) -> dict:
        return self._create_custom_field_groups("customers", groups)

    async def _create_custom_field_groups_async(
        self, entity_type: str, groups: list
    ) -> dict:
        """Async version of _create_custom_field_groups."""
        url = f"{self.crm_url}/api/v4/{entity_type}/custom_fields/groups"
        return await self._send_api_request_async("post", url, groups)

    async def create_leads_custom_field_groups_async(self, groups: list) -> dict:
        return await self._create_custom_field_groups_async("leads", groups)

    async def create_contacts_custom_field_groups_async(self, groups: list) -> dict:
        return await self._create_custom_field_groups_async("contacts", groups)

    async def create_companies_custom_field_groups_async(self, groups: list) -> dict:
        return await self._create_custom_field_groups_async("companies", groups)

    async def create_customers_custom_field_groups_async(self, groups: list) -> dict:
        return await self._create_custom_field_groups_async("customers", groups)

    def _update_custom_field_groups(
        self, entity_type: str, group_id: str, group: dict
    ) -> dict:
        """Update custom field group by id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/custom-fields#custom-field-groups
        """
        url = (
            f"{self.crm_url}/api/v4/{entity_type}/custom_fields/groups/{group_id}"
        )
        return self._send_api_request("patch", url, group)

    def update_leads_custom_field_group(self, group_id: str, group: dict) -> dict:
        return self._update_custom_field_groups("leads", group_id, group)

    def update_contacts_custom_field_group(self, group_id: str, group: dict) -> dict:
        return self._update_custom_field_groups("contacts", group_id, group)

    def update_companies_custom_field_group(self, group_id: str, group: dict) -> dict:
        return self._update_custom_field_groups("companies", group_id, group)

    def update_customers_custom_field_group(self, group_id: str, group: dict) -> dict:
        return self._update_custom_field_groups("customers", group_id, group)

    async def _update_custom_field_groups_async(
        self, entity_type: str, group_id: str, group: dict
    ) -> dict:
        """Async version of _update_custom_field_groups."""
        url = (
            f"{self.crm_url}/api/v4/{entity_type}/custom_fields/groups/{group_id}"
        )
        return await self._send_api_request_async("patch", url, group)

    async def update_leads_custom_field_group_async(
        self, group_id: str, group: dict
    ) -> dict:
        return await self._update_custom_field_groups_async("leads", group_id, group)

    async def update_contacts_custom_field_group_async(
        self, group_id: str, group: dict
    ) -> dict:
        return await self._update_custom_field_groups_async("contacts", group_id, group)

    async def update_companies_custom_field_group_async(
        self, group_id: str, group: dict
    ) -> dict:
        return await self._update_custom_field_groups_async("companies", group_id, group)

    async def update_customers_custom_field_group_async(
        self, group_id: str, group: dict
    ) -> dict:
        return await self._update_custom_field_groups_async("customers", group_id, group)

    def _delete_custom_field_group(
        self, entity_type: str, group_id: str
    ) -> dict:
        """Delete custom field group by id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/custom-fields#custom-field-groups
        """
        url = (
            f"{self.crm_url}/api/v4/{entity_type}/custom_fields/groups/{group_id}"
        )
        return self._send_api_request("delete", url)

    def delete_leads_custom_field_group(self, group_id: str) -> dict:
        return self._delete_custom_field_group("leads", group_id)

    def delete_contacts_custom_field_group(self, group_id: str) -> dict:
        return self._delete_custom_field_group("contacts", group_id)

    def delete_companies_custom_field_group(self, group_id: str) -> dict:
        return self._delete_custom_field_group("companies", group_id)

    def delete_customers_custom_field_group(self, group_id: str) -> dict:
        return self._delete_custom_field_group("customers", group_id)

    async def _delete_custom_field_group_async(
        self, entity_type: str, group_id: str
    ) -> dict:
        """Async version of _delete_custom_field_group."""
        url = (
            f"{self.crm_url}/api/v4/{entity_type}/custom_fields/groups/{group_id}"
        )
        return await self._send_api_request_async("delete", url)

    async def delete_leads_custom_field_group_async(self, group_id: str) -> dict:
        return await self._delete_custom_field_group_async("leads", group_id)

    async def delete_contacts_custom_field_group_async(self, group_id: str) -> dict:
        return await self._delete_custom_field_group_async("contacts", group_id)

    async def delete_companies_custom_field_group_async(self, group_id: str) -> dict:
        return await self._delete_custom_field_group_async("companies", group_id)

    async def delete_customers_custom_field_group_async(self, group_id: str) -> dict:
        return await self._delete_custom_field_group_async("customers", group_id)
