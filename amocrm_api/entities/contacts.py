
from collections.abc import AsyncIterator, Iterator
from urllib.parse import urlencode

from .base import Entity


class Contacts(Entity):
    def _build_get_contacts_chats_url(
        self,
        page: int | None,
        limit: int | None,
        filter_by_chat_ids: str | list | None,
        filter_by_contact_ids: int | list | None,
    ) -> str:
        url = f"{self.crm_url}/api/v4/contacts/chats"
        params: dict = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if filter_by_chat_ids:
            params["filter[chat_id][]" if isinstance(filter_by_chat_ids, list) else "filter[chat_id]"] = (
                filter_by_chat_ids
            )
        if filter_by_contact_ids:
            params["filter[contact_id][]" if isinstance(filter_by_contact_ids, list) else "filter[contact_id]"] = (
                filter_by_contact_ids
            )
        return f"{url}?{urlencode(params, doseq=True)}"

    def get_contacts_chats(
        self,
        page: int | None = None,
        limit: int | None = None,
        filter_by_chat_ids: str | list | None = None,
        filter_by_contact_ids: int | list | None = None,
    ) -> dict:
        """Get chats related to contacts
        Doc: https://www.amocrm.ru/developers/content/crm_platform/contacts-api#contacts-chats
        Args:
            page (Optional[int], optional): page number. Defaults to None.
            limit (Optional[int], optional): limit of rows. Defaults to None.
            filter_by_chat_ids (Union[str, list, None], optional): chat uuids filter. Defaults to None.
            filter_by_contact_ids (Union[int, list, None], optional): contact ids filter. Defaults to None.
        """
        url = self._build_get_contacts_chats_url(
            page, limit, filter_by_chat_ids, filter_by_contact_ids
        )
        return self._send_api_request("get", url)

    def create_contacts_chats(self, objects: list) -> dict:
        """Bind chats to contacts
        Doc: https://www.amocrm.ru/developers/content/crm_platform/contacts-api#contacts-chats
        Args:
            objects (list): list of {'contact_id': int, 'chat_id': str, 'request_id': str}
        """
        url = f"{self.crm_url}/api/v4/contacts/chats"
        return self._send_api_request("post", url, objects)

    def unlink_contacts_entity(self, entity_id: int, objects: list) -> dict:
        return self._unlink_entities("contacts", entity_id, objects)

    def link_contacts_entity(self, entity_id: int, objects: list) -> dict:
        return self._link_entities("contacts", entity_id, objects)

    def get_contacts_links(
        self, entity_id: int, filters: dict | None = None
    ) -> dict:
        return self._get_entity_links("contacts", entity_id, filters)

    def get_contacts(
        self,
        limit: int = 250,
        page: int = 1,
        with_params: list | None = None,
        filters: dict | None = None,
        order: dict | None = None,
        query: str | None = None,
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

    async def get_contacts_chats_async(
        self,
        page: int | None = None,
        limit: int | None = None,
        filter_by_chat_ids: str | list | None = None,
        filter_by_contact_ids: int | list | None = None,
    ) -> dict:
        """Async version of get_contacts_chats."""
        url = self._build_get_contacts_chats_url(
            page, limit, filter_by_chat_ids, filter_by_contact_ids
        )
        return await self._send_api_request_async("get", url)

    async def create_contacts_chats_async(self, objects: list) -> dict:
        """Async version of create_contacts_chats."""
        url = f"{self.crm_url}/api/v4/contacts/chats"
        return await self._send_api_request_async("post", url, objects)

    async def unlink_contacts_entity_async(
        self, entity_id: int, objects: list
    ) -> dict:
        """Async version of unlink_contacts_entity."""
        return await self._unlink_entities_async("contacts", entity_id, objects)

    async def link_contacts_entity_async(
        self, entity_id: int, objects: list
    ) -> dict:
        """Async version of link_contacts_entity."""
        return await self._link_entities_async("contacts", entity_id, objects)

    async def get_contacts_links_async(
        self, entity_id: int, filters: dict | None = None
    ) -> dict:
        """Async version of get_contacts_links."""
        return await self._get_entity_links_async("contacts", entity_id, filters)

    async def get_contacts_async(
        self,
        limit: int = 250,
        page: int = 1,
        with_params: list | None = None,
        filters: dict | None = None,
        order: dict | None = None,
        query: str | None = None,
    ) -> dict:
        """Async version of get_contacts."""
        params = {k: v for k, v in locals().items() if k != "self"}
        return await self._get_entities_async("contacts", **params)

    def iter_contacts(
        self,
        limit: int = 250,
        with_params: list | None = None,
        filters: dict | None = None,
        order: dict | None = None,
        query: str | None = None,
    ) -> Iterator[dict]:
        """Iterate over all contacts across pages."""
        return self._iter_entities(
            "contacts", limit, with_params, filters, None, order, "contacts", query
        )

    async def iter_contacts_async(
        self,
        limit: int = 250,
        with_params: list | None = None,
        filters: dict | None = None,
        order: dict | None = None,
        query: str | None = None,
    ) -> AsyncIterator[dict]:
        """Async version of iter_contacts."""
        async for contact in self._iter_entities_async(
            "contacts", limit, with_params, filters, None, order, "contacts", query
        ):
            yield contact

    async def get_contact_async(self, contact_id: int) -> dict:
        """Async version of get_contact."""
        url = f"{self.crm_url}/api/v4/contacts/{contact_id}"
        return await self._send_api_request_async("get", url)

    async def create_contacts_async(self, contacts: list) -> dict:
        """Async version of create_contacts."""
        return await self._create_or_update_entities_async("contacts", contacts)

    async def update_contacts_async(self, contacts: list) -> dict:
        """Async version of update_contacts."""
        return await self._create_or_update_entities_async("contacts", contacts, True)
