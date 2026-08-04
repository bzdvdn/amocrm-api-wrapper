from .base import Entity

from typing import Optional

class Contacts(Entity):
    def unlink_contacts_entity(self, entity_id: int, objects: list) -> dict:
        return self._unlink_entities("contacts", entity_id, objects)

    def link_contacts_entity(self, entity_id: int, objects: list) -> dict:
        return self._link_entities("contacts", entity_id, objects)

    def get_contacts_links(
        self, entity_id: int, filters: Optional[dict] = None
    ) -> dict:
        return self._get_entity_links("contacts", entity_id, filters)

    def get_contacts(
        self,
        limit: int = 250,
        page: int = 1,
        with_params: Optional[list] = None,
        filters: Optional[dict] = None,
        order: Optional[dict] = None,
    ) -> dict:
        """Get contacts
        Doc: https://www.amocrm.ru/developers/content/crm_platform/contacts-api#contacts-list
        Args:
            limit (int, optional): limit of rows. Defaults to 250.
            page (int, optional): number of page. Defaults to 1.
            with_params (Optional[list], optional): params. Defaults to None.
            filters (Optional[dict], optional): filter params like {'[updated_at][from]': '<timestamp>'}. Defaults to None.
            order (Optional[dict], optional): filter params like {'updated_at': 'asc'}. Defaults to None.
        Returns:
            dict:{
                "_page": 1,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/contacts?limit=2&page=1"
                    },
                    "next": {
                        "href": "https://example.amocrm.ru/api/v4/contacts?limit=2&page=2"
                    }
                },
                "_embedded": {
                    "contacts": [
                        {
                            "id": 7143599,
                            "name": "1",
                            "first_name": "",
                            "last_name": "",
                            "responsible_user_id": 504141,
                            "group_id": 0,
                            "created_by": 504141,
                            "updated_by": 504141,
                            "created_at": 1585758065,
                            "updated_at": 1585758065,
                            "closest_task_at": null,
                            "custom_fields_values": null,
                            "account_id": 28805383,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/contacts/7143599"
                                }
                            },
                            "_embedded": {
                                "tags": [],
                                "companies": []
                            }
                        },
                        {
                            "id": 7767065,
                            "name": "dsgdsg",
                            "first_name": "",
                            "last_name": "",
                            "responsible_user_id": 504141,
                            "group_id": 0,
                            "created_by": 504141,
                            "updated_by": 504141,
                            "created_at": 1586359590,
                            "updated_at": 1586359590,
                            "closest_task_at": null,
                            "custom_fields_values": null,
                            "account_id": 28805383,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/contacts/7767065"
                                }
                            },
                            "_embedded": {
                                "tags": [],
                                "companies": []
                            }
                        }
                    ]
                }
            }
        """
        params = {k: v for k, v in locals().items() if k != "self"}
        return self._get_entities("contacts", **params)

    def get_contact(self, contact_id: int) -> dict:
        """Get contact
        Doc: https://www.amocrm.ru/developers/content/crm_platform/contacts-api#contact-detail
        Args:
            contact_id (int): id of contact
    
        Returns:
            dict: {
                "id": 3,
                "name": "Иван Иванов",
                "first_name": "Иван",
                "last_name": "Иванов",
                "responsible_user_id": 504141,
                "group_id": 0,
                "created_by": 504141,
                "updated_by": 504141,
                "created_at": 1582117331,
                "updated_at": 1590943929,
                "closest_task_at": null,
                "custom_fields_values": [
                    {
                        "field_id": 3,
                        "field_name": "Телефон",
                        "field_code": "PHONE",
                        "field_type": "multitext",
                        "values": [
                            {
                                "value": "+79123",
                                "enum_id": 1,
                                "enum": "WORK"
                            }
                        ]
                    }
                ],
                "account_id": 28805383,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/contacts/3"
                    }
                },
                "_embedded": {
                    "tags": [],
                    "leads": [
                        {
                            "id": 1,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/1"
                                }
                            }
                        },
                        {
                            "id": 3916883,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/3916883"
                                }
                            }
                        }
                    ],
                    "customers": [
                        {
                            "id": 134923,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/customers/134923"
                                }
                            }
                        }
                    ],
                    "catalog_elements": [],
                    "companies": [
                        {
                            "id": 1,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/companies/1"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = f"{self.crm_url}/api/v4/contacts/{contact_id}"
        return self._send_api_request("get", url)

    def create_contacts(self, contacts: list) -> dict:
        """Create contacts
        Doc: https://www.amocrm.ru/developers/content/crm_platform/contacts-api#contacts-add
        Args:
            contacts (list): list of contacts objects
    
        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/contacts"
                    }
                },
                "_embedded": {
                    "contacts": [
                        {
                            "id": 40401635,
                            "request_id": "0",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/contacts/40401635"
                                }
                            },
                            {
                                "id": 40401636,
                                "request_id": "1",
                                "_links": {
                                    "self": {
                                    "href": "https://example.amocrm.ru/api/v4/contacts/40401636"
                            }
                            }
                        }
                    ]
                }
            }
        """
        return self._create_or_update_entities("contacts", contacts)

    def update_contacts(self, contacts: list) -> dict:
        """Update contacts
    
        Args:
            contacts (list): list of contacts object
    
        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/contacts"
                    }
                },
                "_embedded": {
                    "contacts": [
                        {
                            "id": 3,
                            "name": "Иван Иванов",
                            "updated_at": 1590945248,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/contacts/3"
                                }
                            }
                        }
                    ]
                }
            }
        """
        return self._create_or_update_entities("contacts", contacts, True)
