
from collections.abc import AsyncIterator, Iterator

from .base import Entity


class Catalogs(Entity):
    def get_catalogs(self, page: int = 1, limit: int = 250) -> dict:
        """Get catalogs
        Doc: https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#lists-list
        Args:
            page (int, optional): page number. Defaults to 1.
            limit (int, optional): limit of page result. Defaults to 250.
    
        Returns:
            dict: {
                "_page": 1,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/catalogs?page=1&limit=50"
                    },
                    "next": {
                        "href": "https://example.amocrm.ru/api/v4/catalogs?page=2&limit=50"
                    }
                },
                "_embedded": {
                    "catalogs": [
                        {
                            "id": 4589,
                            "name": "Просто список",
                            "created_by": 504141,
                            "updated_by": 504141,
                            "created_at": 1590742040,
                            "updated_at": 1590742040,
                            "sort": 10,
                            "type": "regular",
                            "can_add_elements": true,
                            "can_show_in_cards": false,
                            "can_link_multiple": true,
                            "can_be_deleted": true,
                            "sdk_widget_code": null,
                            "account_id": 28805383,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/catalogs/4589"
                                }
                            }
                        },
                        {
                            "id": 4521,
                            "name": "Товары",
                            "created_by": 504141,
                            "updated_by": 504141,
                            "created_at": 1589390310,
                            "updated_at": 1590742040,
                            "sort": 20,
                            "type": "products",
                            "can_add_elements": true,
                            "can_show_in_cards": false,
                            "can_link_multiple": true,
                            "can_be_deleted": false,
                            "sdk_widget_code": null,
                            "account_id": 28805383,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/catalogs/4521"
                                }
                            }
                        },
                        {
                            "id": 4517,
                            "name": "Счета",
                            "created_by": 504141,
                            "updated_by": 504141,
                            "created_at": 1589379462,
                            "updated_at": 1590742040,
                            "sort": 30,
                            "type": "invoices",
                            "can_add_elements": false,
                            "can_show_in_cards": false,
                            "can_link_multiple": true,
                            "can_be_deleted": true,
                            "sdk_widget_code": null,
                            "account_id": 28805383,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/catalogs/4517"
                                }
                            }
                        }
                    ]
                }
            }
        """
        params: dict = {"page": page, "limit": limit}
        return self._get_entities("catalogs", **params)

    def get_catalog(self, catalog_id: int) -> dict:
        """Get catalog
        Doc: https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#list-detail
        Args:
            catalog_id (int): id of catalog
    
        Returns:
            dict: {
                "id": 4589,
                "name": "Просто список",
                "created_by": 504141,
                "updated_by": 504141,
                "created_at": 1590742040,
                "updated_at": 1590742040,
                "sort": 10,
                "type": "regular",
                "can_add_elements": true,
                "can_show_in_cards": false,
                "can_link_multiple": true,
                "can_be_deleted": true,
                "sdk_widget_code": null,
                "account_id": 28805383,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/catalogs/4589"
                    }
                }
            }
        """
        url = f"{self.crm_url}/api/v4/catalogs/{catalog_id}"
        return self._send_api_request("get", url)

    def create_catalogs(self, catalogs: list) -> dict:
        """Create catalogs
        Doc: https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#lists-add
        Args:
            catalogs (list): list of catalogs
    
        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/catalogs"
                    }
                },
                "_embedded": {
                    "catalogs": [
                        {
                            "id": 5785,
                            "name": "Тестовый список",
                            "created_by": 3944275,
                            "updated_by": 3944275,
                            "created_at": 1589397957,
                            "updated_at": 1589397957,
                            "sort": 10,
                            "type": "regular",
                            "can_add_elements": true,
                            "can_show_in_cards": false,
                            "can_link_multiple": false,
                            "can_be_deleted": true,
                            "account_id": 123123,
                            "request_id": "123",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/catalogs/5785"
                                }
                            }
                        }
                    ]
                }
            }
        """
        return self._create_or_update_entities("catalogs", catalogs)

    def update_catalogs(self, catalogs: list) -> dict:
        """Update catalogs
        Doc: https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#lists-edit
        Args:
            catalogs (list): list of catalogs
    
        Returns:
            dict: {
                "id": 5787,
                "name": "Новое имя списка",
                "created_by": 3944275,
                "updated_by": 3944275,
                "created_at": 1589399557,
                "updated_at": 1589399886,
                "sort": 30,
                "type": "regular",
                "can_add_elements": true,
                "can_show_in_cards": false,
                "can_link_multiple": false,
                "can_be_deleted": true,
                "account_id": 123123,
                "request_id": "5787",
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/catalogs/5787"
                    }
                }
            }
        """
        return self._create_or_update_entities("catalogs", catalogs, True)

    def get_catalog_elements(
        self,
        catalog_id: int,
        page: int = 1,
        limit: int = 250,
        filters: dict | None = None,
        query: str | None = None,
    ) -> dict:
        """Get elements by catalog id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#list-elements-list
        Args:
            catalog_id (int): id of catalog
            page (int, optional): number of page. Defaults to 1.
            limit (int, optional): limit rows. Defaults to 250.
            filters (Optional[dict], optional): filter dict. Defaults to None.
            query (Optional[str], optional): search query. Defaults to None.
    
        Returns:
            dict: {
                "_page": 1,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/catalogs/4521/elements?page=1&limit=50"
                    },
                    "next": {
                        "href": "https://example.amocrm.ru/api/v4/catalogs/4521/elements?page=2&limit=50"
                    }
                },
                "_embedded": {
                    "elements": [
                        {
                            "id": 525439,
                            "name": "Элемент",
                            "created_by": 504141,
                            "updated_by": 504141,
                            "created_at": 1589390333,
                            "updated_at": 1590683336,
                            "is_deleted": null,
                            "custom_fields_values": [
                                {
                                    "field_id": 271207,
                                    "field_name": "Артикул",
                                    "field_code": "SKU",
                                    "field_type": "text",
                                    "values": [
                                        {
                                            "value": "dsg"
                                        }
                                    ]
                                },
                                {
                                    "field_id": 271209,
                                    "field_name": "Описание",
                                    "field_code": "DESCRIPTION",
                                    "field_type": "textarea",
                                    "values": [
                                        {
                                            "value": "Описание"
                                        }
                                    ]
                                },
                                {
                                    "field_id": 271211,
                                    "field_name": "Цена",
                                    "field_code": "PRICE",
                                    "field_type": "numeric",
                                    "values": [
                                        {
                                            "value": "12"
                                        }
                                    ]
                                },
                                {
                                    "field_id": 271213,
                                    "field_name": "Группа",
                                    "field_code": "GROUP",
                                    "field_type": "category",
                                    "values": [
                                        {
                                            "value": "Телефоны",
                                            "enum_id": 10663
                                        }
                                    ]
                                }
                            ],
                            "catalog_id": 4521,
                            "account_id": 28805383,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/catalogs/4521/elements/525439"
                                }
                            }
                        }
                    ]
                }
            }
        """
        params: dict = {
            "page": page,
            "limit": limit,
            "filters": filters,
            "query": query,
        }
        entity = f"catalogs/{catalog_id}/elements"
        return self._get_entities(entity, **params)

    def get_catalog_element(self, catalog_id: int, element_id: int) -> dict:
        """Get catalog element
        Doc: https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#list-elements-detail
        Args:
            catalog_id (int): id of catalog
            element_id (int): id of element
    
        Returns:
            dict: {
                "id": 525439,
                "name": "Элемент",
                "created_by": 504141,
                "updated_by": 504141,
                "created_at": 1589390333,
                "updated_at": 1590683336,
                "is_deleted": null,
                "custom_fields_values": [
                    {
                        "field_id": 271207,
                        "field_name": "Артикул",
                        "field_code": "SKU",
                        "field_type": "text",
                        "values": [
                            {
                                "value": "dsg"
                            }
                        ]
                    },
                    {
                        "field_id": 271209,
                        "field_name": "Описание",
                        "field_code": "DESCRIPTION",
                        "field_type": "textarea",
                        "values": [
                            {
                                "value": "Супер телефон"
                            }
                        ]
                    },
                    {
                        "field_id": 271211,
                        "field_name": "Цена",
                        "field_code": "PRICE",
                        "field_type": "numeric",
                        "values": [
                            {
                                "value": "12"
                            }
                        ]
                    },
                    {
                        "field_id": 271213,
                        "field_name": "Группа",
                        "field_code": "GROUP",
                        "field_type": "category",
                        "values": [
                            {
                                "value": "Телефоны",
                                "enum_id": 10663
                            }
                        ]
                    }
                ],
                "catalog_id": 4521,
                "account_id": 28805383,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/catalogs/4521/elements/525439"
                    }
                }
            }
        """
        url = f"{self.crm_url}/api/v4/catalogs/{catalog_id}/elements/{element_id}"
        return self._send_api_request("get", url)

    def add_elements_to_catalog(self, catalog_id: int, elements: list) -> dict:
        """Add elements to catalog
        Doc: https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#list-elements-add
        Args:
            catalog_id (int): id of catalog
            elements (list): list of elements
    
        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/catalogs/1209/elements"
                    }
                },
                "_embedded": {
                    "elements": [
                        {
                            "id": 986757,
                            "name": "Новый элемент списка",
                            "created_by": 3944275,
                            "updated_by": 3944275,
                            "created_at": 1589294541,
                            "updated_at": 1589294541,
                            "is_deleted": false,
                            "custom_fields_values": [
                                {
                                    "field_id": 14687,
                                    "field_name": "Цена",
                                    "field_code": "PRICE",
                                    "field_type": "numeric",
                                    "values": [
                                        {
                                            "value": "1000"
                                        }
                                    ]
                                }
                            ],
                            "catalog_id": 1209,
                            "account_id": 123123,
                            "request_id": 0,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/catalogs/1209/elements/986757"
                                }
                            }
                        }
                    ]
                }
            }
        """
        return self._create_or_update_entities(
            f"catalogs/{catalog_id}/elements", elements
        )

    def update_elements_in_catalog(self, catalog_id: int, elements: list) -> dict:
        """Add elements to catalog
        Doc: https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#list-elements-edit
        Args:
            catalog_id (int): id of catalog
            elements (list): list of elements
    
        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/catalogs/1209/elements"
                    }
                },
                "_embedded": {
                    "elements": [
                        {
                            "id": 986757,
                            "name": "Новое имя элемента",
                            "created_by": 3944275,
                            "updated_by": 3944275,
                            "created_at": 1589294541,
                            "updated_at": 1589295769,
                            "is_deleted": false,
                            "custom_fields_values": [ ],
                            "catalog_id": 1209,
                            "account_id": 123123,
                            "request_id": 986757,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/catalogs/1209/elements/986757"
                                }
                            }
                        },
                        {
                            "id": 986753,
                            "name": "Новое имя элемента 2",
                            "created_by": 3944275,
                            "updated_by": 3944275,
                            "created_at": 1589294429,
                            "updated_at": 1589295769,
                            "is_deleted": false,
                            "custom_fields_values": [],
                            "catalog_id": 1209,
                            "account_id": 123123,
                            "request_id": 986753,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/catalogs/1209/elements/986753"
                                }
                            }
                        }
                    ]
                }
            }
        """
        return self._create_or_update_entities(
            f"catalogs/{catalog_id}/elements", elements, True
        )

    async def get_catalogs_async(self, page: int = 1, limit: int = 250) -> dict:
        """Async version of get_catalogs."""
        params: dict = {"page": page, "limit": limit}
        return await self._get_entities_async("catalogs", **params)

    async def get_catalog_async(self, catalog_id: int) -> dict:
        """Async version of get_catalog."""
        url = f"{self.crm_url}/api/v4/catalogs/{catalog_id}"
        return await self._send_api_request_async("get", url)

    async def create_catalogs_async(self, catalogs: list) -> dict:
        """Async version of create_catalogs."""
        return await self._create_or_update_entities_async("catalogs", catalogs)

    async def update_catalogs_async(self, catalogs: list) -> dict:
        """Async version of update_catalogs."""
        return await self._create_or_update_entities_async("catalogs", catalogs, True)

    async def get_catalog_elements_async(
        self,
        catalog_id: int,
        page: int = 1,
        limit: int = 250,
        filters: dict | None = None,
        query: str | None = None,
    ) -> dict:
        """Async version of get_catalog_elements."""
        params: dict = {
            "page": page,
            "limit": limit,
            "filters": filters,
            "query": query,
        }
        entity = f"catalogs/{catalog_id}/elements"
        return await self._get_entities_async(entity, **params)

    def iter_catalog_elements(
        self,
        catalog_id: int,
        limit: int = 250,
        filters: dict | None = None,
    ) -> Iterator[dict]:
        """Iterate over all catalog elements across pages."""
        entity = f"catalogs/{catalog_id}/elements"
        return self._iter_entities(entity, limit, None, filters, None, None, "elements")

    async def iter_catalog_elements_async(
        self,
        catalog_id: int,
        limit: int = 250,
        filters: dict | None = None,
    ) -> AsyncIterator[dict]:
        """Async version of iter_catalog_elements."""
        entity = f"catalogs/{catalog_id}/elements"
        async for element in self._iter_entities_async(
            entity, limit, None, filters, None, None, "elements"
        ):
            yield element

    async def get_catalog_element_async(
        self, catalog_id: int, element_id: int
    ) -> dict:
        """Async version of get_catalog_element."""
        url = (
            f"{self.crm_url}/api/v4/catalogs/{catalog_id}/elements/{element_id}"
        )
        return await self._send_api_request_async("get", url)

    async def add_elements_to_catalog_async(
        self, catalog_id: int, elements: list
    ) -> dict:
        """Async version of add_elements_to_catalog."""
        return await self._create_or_update_entities_async(
            f"catalogs/{catalog_id}/elements", elements
        )

    async def update_elements_in_catalog_async(
        self, catalog_id: int, elements: list
    ) -> dict:
        """Async version of update_elements_in_catalog."""
        return await self._create_or_update_entities_async(
            f"catalogs/{catalog_id}/elements", elements, True
        )
