from .base import Entity

from typing import Optional

class CustomFields(Entity):
    def _get_custom_fields(self, entity: str, page: Optional[int] = None) -> dict:
        url = f"{self.crm_url}/api/v4/{entity}/custom_fields"
        if page:
            url = f"{url}?page={page}"
        return self._send_api_request("get", url)

    def get_contacts_custom_fields(self, page: Optional[int] = None) -> dict:
        return self._get_custom_fields("contacts", page=page)

    def get_leads_custom_fields(self, page: Optional[int] = None) -> dict:
        return self._get_custom_fields("leads", page=page)

    def get_companies_custom_fields(self, page: Optional[int] = None) -> dict:
        return self._get_custom_fields("companies", page=page)

    def get_customers_custom_fields(self, page: Optional[int] = None) -> dict:
        return self._get_custom_fields("customers", page=page)

    def get_customer_segments_custom_fields(self, page: Optional[int] = None) -> dict:
        return self._get_custom_fields("customers/segments", page=page)

    def get_catalog_custom_fields(self, catalog_id: str) -> dict:
        return self._get_custom_fields(f"catalogs/{catalog_id}")

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
