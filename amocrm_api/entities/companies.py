from .base import Entity

from typing import Optional

class Companies(Entity):
    def unlink_companies_entity(self, entity_id: int, objects: list) -> dict:
        return self._unlink_entities("companies", entity_id, objects)

    def link_companies_entity(self, entity_id: int, objects: list) -> dict:
        return self._link_entities("companies", entity_id, objects)

    def get_companies_links(
        self, entity_id: int, filters: Optional[dict] = None
    ) -> dict:
        return self._get_entity_links("companies", entity_id, filters)

    def get_companies(
        self,
        limit: int = 250,
        page: int = 1,
        with_params: Optional[list] = None,
        filters: Optional[dict] = None,
        order: Optional[dict] = None,
    ) -> dict:
        """Get companies
        Doc: https://www.amocrm.ru/developers/content/crm_platform/companies-api#companies-list
        Args:
            limit (int, optional): limit of page. Defaults to 250.
            page (int, optional): page index. Defaults to 1.
            with_params (Optional[list], optional): with params(check dock). Defaults to None.
            filters (Optional[dict], optional): dict filters like({'[updated_at][from]: "<timestamp>"'}). Defaults to None.
            order (Optional[dict], optional): dict like - {'updated_at': 'asc'}. Defaults to None.
    
        Returns:
            dict: {
                "_page": 1,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/companies?limit=2&page=1"
                    },
                    "next": {
                        "href": "https://example.amocrm.ru/api/v4/companies?limit=2&page=2"
                    }
                },
                "_embedded": {
                    "companies": [
                            {
                                "id": 7767077,
                                "name": "Компания Васи",
                                "responsible_user_id": 504141,
                                "group_id": 0,
                                "created_by": 504141,
                                "updated_by": 504141,
                                "created_at": 1586359618,
                                "updated_at": 1586359618,
                                "closest_task_at": null,
                                "custom_fields_values": null,
                                "account_id": 28805383,
                                "_links": {
                                    "self": {
                                        "href": "https://example.amocrm.ru/api/v4/companies/7767077"
                                    }
                                },
                                "_embedded": {
                                    "tags": []
                                }
                            },
                            {
                                "id": 7767457,
                                "name": "Example",
                                "responsible_user_id": 504141,
                                "group_id": 0,
                                "created_by": 504141,
                                "updated_by": 504141,
                                "created_at": 1586360394,
                                "updated_at": 1586360394,
                                "closest_task_at": null,
                                "custom_fields_values": null,
                                "account_id": 28805383,
                                "_links": {
                                    "self": {
                                        "href": "https://example.amocrm.ru/api/v4/companies/7767457"
                                    }
                                },
                                "_embedded": {
                                    "tags": []
                                }
                            }
                        ]
                    }
                }
        """
        params = {k: v for k, v in locals().items() if k != "self"}
        return self._get_entities("companies", **params)

    def get_company(self, company_id: int) -> dict:
        """Get company
        Doc: https://www.amocrm.ru/developers/content/crm_platform/companies-api#company-detail
        Args:
            company_id (int): id of company
    
        Returns:
            dict: {
                "id": 1,
                "name": "АО Рога и копыта",
                "responsible_user_id": 504141,
                "group_id": 0,
                "created_by": 504141,
                "updated_by": 504141,
                "created_at": 1582117331,
                "updated_at": 1586361223,
                "closest_task_at": null,
                "custom_fields_values": [
                    {
                        "field_id": 3,
                        "field_name": "Телефон",
                        "field_code": "PHONE",
                        "field_type": "multitext",
                        "values": [
                            {
                                "value": "123213",
                                "enum_id": 1,
                                "enum": "WORK"
                            }
                        ]
                    }
                ],
                "account_id": 28805383,
                "_links": {
                    "self": {
                        "href": "https://exmaple.amocrm.ru/api/v4/companies/1"
                    }
                },
                "_embedded": {
                    "tags": []
                }
            }
        """
        url = f"{self.crm_url}/api/v4/companies/{company_id}"
        return self._send_api_request("get", url)

    def create_companies(self, companies: list) -> dict:
        """Create companies
        Doc: https://www.amocrm.ru/developers/content/crm_platform/companies-api#companies-add
        Args:
            companies (list): list of companies
    
        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/companies"
                    }
                },
                "_embedded": {
                    "companies": [
                        {
                            "id": 11090825,
                            "request_id": "0",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/companies/11090825"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = f"{self.crm_url}/api/v4/companies"
        return self._send_api_request("post", url, companies)

    async def unlink_companies_entity_async(
        self, entity_id: int, objects: list
    ) -> dict:
        """Async version of unlink_companies_entity."""
        return await self._unlink_entities_async("companies", entity_id, objects)

    async def link_companies_entity_async(
        self, entity_id: int, objects: list
    ) -> dict:
        """Async version of link_companies_entity."""
        return await self._link_entities_async("companies", entity_id, objects)

    async def get_companies_links_async(
        self, entity_id: int, filters: Optional[dict] = None
    ) -> dict:
        """Async version of get_companies_links."""
        return await self._get_entity_links_async("companies", entity_id, filters)

    async def get_companies_async(
        self,
        limit: int = 250,
        page: int = 1,
        with_params: Optional[list] = None,
        filters: Optional[dict] = None,
        order: Optional[dict] = None,
    ) -> dict:
        """Async version of get_companies."""
        params = {k: v for k, v in locals().items() if k != "self"}
        return await self._get_entities_async("companies", **params)

    async def get_company_async(self, company_id: int) -> dict:
        """Async version of get_company."""
        url = f"{self.crm_url}/api/v4/companies/{company_id}"
        return await self._send_api_request_async("get", url)

    async def create_companies_async(self, companies: list) -> dict:
        """Async version of create_companies."""
        url = f"{self.crm_url}/api/v4/companies"
        return await self._send_api_request_async("post", url, companies)

    async def update_companies_async(self, companies: list) -> dict:
        """Async version of update_companies."""
        url = f"{self.crm_url}/api/v4/companies"
        return await self._send_api_request_async("post", url, companies)

    def update_companies(self, companies: list) -> dict:
        """Update companies

        Args:
            companies (list): list of companies

        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/companies"
                    }
                },
                "_embedded": {
                    "companies": [
                        {
                            "id": 11090825,
                            "name": "Новое название компании",
                            "updated_at": 1590998669,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/companies/11090825"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = f"{self.crm_url}/api/v4/companies"
        return self._send_api_request("post", url, companies)
