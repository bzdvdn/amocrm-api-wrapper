
from collections.abc import AsyncIterator, Iterator

from .base import Entity


class Leads(Entity):
    def link_leads_entity(self, entity_id: int, objects: list) -> dict:
        return self._link_entities("leads", entity_id, objects)

    def unlink_leads_entity(self, entity_id: int, objects: list) -> dict:
        return self._unlink_entities("leads", entity_id, objects)

    def get_leads_links(self, entity_id: int, filters: dict | None = None) -> dict:
        return self._get_entity_links("leads", entity_id, filters)

    def create_leads(self, objects: list) -> dict:
        """create leads
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads-api#leads-add
        Args:
            objects (list): list of leads
    
        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads"
                    }
                },
                "_embedded": {
                    "leads": [
                        {
                            "id": 10185151,
                            "request_id": "0",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/10185151"
                                }
                            }
                        },
                        {
                            "id": 10185153,
                            "request_id": "1",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/10185153"
                                }
                            }
                        }
                    ]
                }
            }
        """
        return self._create_or_update_entities("leads", objects)

    def create_leads_complex(self, objects: list) -> dict:
        """Create complex leads with nested entities (contacts, companies, notes, tasks).
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads-api#leads-complex
        Args:
            objects (list): list of complex leads

        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/complex"
                    }
                },
                "_embedded": {
                    "leads": [
                        {
                            "id": 10185151,
                            "request_id": "0",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/10185151"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = f"{self.crm_url}/api/v4/leads/complex"
        return self._send_api_request("post", url, data=objects)

    def update_leads(self, objects: list) -> dict:
        """update leads
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads-api#leads-edit
        Args:
            objects (list): list of leads
        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads"
                    }
                },
                "_embedded": {
                    "leads": [
                        {
                            "id": 54886,
                            "updated_at": 1589556420,
                            "request_id": "0",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/54886"
                                }
                            }
                        },
                        {
                            "id": 54884,
                            "updated_at": 1589556420,
                            "request_id": "1",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/54884"
                                }
                            }
                        }
                    ]
                }
            }
        """
        return self._create_or_update_entities("leads", objects, True)

    def get_lead(self, lead_id: int, with_params: list | None = None) -> dict:
        """return lead
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads-api#lead-detail
        Args:
            lead_id (int): id of lead
    
        Returns:
            dict: {
                "id": 3912171,
                "name": "Example",
                "price": 12,
                "responsible_user_id": 504141,
                "group_id": 0,
                "status_id": 143,
                "pipeline_id": 3104455,
                "loss_reason_id": 4203748,
                "source_id": null,
                "created_by": 504141,
                "updated_by": 504141,
                "created_at": 1585299171,
                "updated_at": 1590683337,
                "closed_at": 1590683337,
                "closest_task_at": null,
                "is_deleted": false,
                "custom_fields_values": null,
                "score": null,
                "account_id": 28805383,
                "is_price_modified_by_robot": false,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/3912171"
                    }
                },
                "_embedded": {
                    "tags": [
                        {
                            "id": 100667,
                            "name": "тест"
                        }
                    ],
                    "catalog_elements": [
                        {
                            "id": 525439,
                            "metadata": {
                                "quantity": 1,
                                "catalog_id": 4521
                            }
                        }
                    ],
                    "loss_reason": [
                        {
                            "id": 4203748,
                            "name": "Пропала потребность",
                            "sort": 100000,
                            "created_at": 1582117280,
                            "updated_at": 1582117280,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/loss_reasons/4203748"
                                }
                            }
                        }
                    ],
                    "companies": [
                        {
                            "id": 10971463,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/companies/10971463"
                                }
                            }
                        }
                    ],
                    "contacts": [
                        {
                            "id": 10971465,
                            "is_main": true,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/contacts/10971465"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = f"{self.crm_url}/api/v4/leads/{lead_id}"
        if with_params:
            url += "?with=" + ",".join(param for param in with_params)
        return self._send_api_request("get", url)

    def get_leads(
        self,
        limit: int = 250,
        page: int = 1,
        with_params: list | None = None,
        filters: dict | None = None,
        filter_ids: list | None = None,
        order: dict | None = None,
        query: str | None = None,
    ) -> dict:
        """Get leads
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads-api#leads-list
        Args:
            limit (int, optional): limit of rows. Defaults to 250.
            page (int, optional): number of page. Defaults to 1.
            with_params (Optional[list], optional): params. Defaults to None.
            filters (Optional[dict], optional): filter params like {'updated_at__from': '<timestamp>', 'updated_at__to': '<timestamp>', 'id': [1, 2]}. Defaults to None.
            filter_ids (Optional[list], optional): filter ids like [1,2,2310]. Defaults to None.
            order (Optional[dict], optional): order params like {'update_at': 'asc'}. Defaults to None.
    
        Returns:
            dict: {
            "_page": 2,
            "_links": {
                "self": {
                    "href": "https://example.amocrm.ru/api/v4/leads?limit=2&page=2"
                },
                "next": {
                    "href": "https://example.amocrm.ru/api/v4/leads?limit=2&page=3"
                },
                "first": {
                    "href": "https://example.amocrm.ru/api/v4/leads?limit=2&page=1"
                },
                "prev": {
                    "href": "https://example.amocrm.ru/api/v4/leads?limit=2&page=1"
                }
            },
            "_embedded": {
                "leads": [
                    {
                        "id": 19619,
                        "name": "Сделка для примера",
                        "price": 46333,
                        "responsible_user_id": 123321,
                        "group_id": 625,
                        "status_id": 142,
                        "pipeline_id": 1300,
                        "loss_reason_id": null,
                        "source_id": null,
                        "created_by": 321123,
                        "updated_by": 321123,
                        "created_at": 1453279607,
                        "updated_at": 1502193501,
                        "closed_at": 1483005931,
                        "closest_task_at": null,
                        "is_deleted": false,
                        "custom_fields_values": null,
                        "score": null,
                        "account_id": 5135160,
                        "_links": {
                            "self": {
                                "href": "https://example.amocrm.ru/api/v4/leads/19619"
                            }
                        },
                        "_embedded": {
                            "tags": [],
                            "companies": []
                        }
                    },
                    {
                        "id": 14460,
                        "name": "Сделка для примера 2",
                        "price": 655,
                        "responsible_user_id": 123321,
                        "group_id": 625,
                        "status_id": 142,
                        "pipeline_id": 1300,
                        "loss_reason_id": null,
                        "source_id": null,
                        "created_by": 321123,
                        "updated_by": 321123,
                        "created_at": 1453279607,
                        "updated_at": 1502193501,
                        "closed_at": 1483005931,
                        "closest_task_at": null,
                        "is_deleted": false,
                        "custom_fields_values": null,
                        "score": null,
                        "account_id": 1351360,
                        "_links": {
                            "self": {
                                "href": "https://example.amocrm.ru/api/v4/leads/14460"
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
        params: dict = {k: v for k, v in locals().items() if k != "self"}
        return self._get_entities("leads", **params)

    async def link_leads_entity_async(
        self, entity_id: int, objects: list
    ) -> dict:
        """Async version of link_leads_entity."""
        return await self._link_entities_async("leads", entity_id, objects)

    async def unlink_leads_entity_async(
        self, entity_id: int, objects: list
    ) -> dict:
        """Async version of unlink_leads_entity."""
        return await self._unlink_entities_async("leads", entity_id, objects)

    async def get_leads_links_async(
        self, entity_id: int, filters: dict | None = None
    ) -> dict:
        """Async version of get_leads_links."""
        return await self._get_entity_links_async("leads", entity_id, filters)

    async def create_leads_async(self, objects: list) -> dict:
        """Async version of create_leads."""
        return await self._create_or_update_entities_async("leads", objects)

    async def create_leads_complex_async(self, objects: list) -> dict:
        """Async version of create_leads_complex."""
        url = f"{self.crm_url}/api/v4/leads/complex"
        return await self._send_api_request_async("post", url, data=objects)

    async def update_leads_async(self, objects: list) -> dict:
        """Async version of update_leads."""
        return await self._create_or_update_entities_async("leads", objects, True)

    async def get_lead_async(
        self, lead_id: int, with_params: list | None = None
    ) -> dict:
        """Async version of get_lead."""
        url = f"{self.crm_url}/api/v4/leads/{lead_id}"
        if with_params:
            url += "?with=" + ",".join(param for param in with_params)
        return await self._send_api_request_async("get", url)

    async def get_leads_async(
        self,
        limit: int = 250,
        page: int = 1,
        with_params: list | None = None,
        filters: dict | None = None,
        filter_ids: list | None = None,
        order: dict | None = None,
        query: str | None = None,
    ) -> dict:
        """Async version of get_leads."""
        params: dict = {k: v for k, v in locals().items() if k != "self"}
        return await self._get_entities_async("leads", **params)

    def iter_leads(
        self,
        limit: int = 250,
        with_params: list | None = None,
        filters: dict | None = None,
        filter_ids: list | None = None,
        order: dict | None = None,
        query: str | None = None,
    ) -> Iterator[dict]:
        """Iterate over all leads across pages."""
        return self._iter_entities(
            "leads", limit, with_params, filters, filter_ids, order, "leads", query
        )

    async def iter_leads_async(
        self,
        limit: int = 250,
        with_params: list | None = None,
        filters: dict | None = None,
        filter_ids: list | None = None,
        order: dict | None = None,
        query: str | None = None,
    ) -> AsyncIterator[dict]:
        """Async version of iter_leads."""
        async for lead in self._iter_entities_async(
            "leads", limit, with_params, filters, filter_ids, order, "leads", query
        ):
            yield lead
