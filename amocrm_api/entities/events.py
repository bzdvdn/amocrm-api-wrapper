from urllib.parse import urlencode

from .base import Entity


class Events(Entity):
    def _build_get_events_type_url(
        self,
        language_code: str | None,
    ) -> str:
        params = {"language_code": language_code}
        return f"{self.crm_url}/api/v4/events/types?{urlencode(params)}"

    def _build_get_events_url(
        self,
        page: int,
        limit: int,
        with_params: list | None,
        filter_by_ids: str | list | None,
        filter_by_created_from: str | list | None,
        filter_by_created_to: str | list | None,
        filter_by_created_by: str | list | None,
        filter_by_entity: str | list | None,
        filter_by_entity_id: str | list | None,
        filter_by_type: str | list | None,
    ) -> str:
        url = f"{self.crm_url}/api/v4/events"
        params: dict = {"limit": limit, "page": page}
        if with_params:
            params["with"] = ",".join(param for param in with_params)
        if filter_by_ids:
            params["filter[id]"] = filter_by_ids
        if filter_by_created_from:
            params["filter[created_at][from]"] = filter_by_created_from
        if filter_by_created_to:
            params["filter[created_at][to]"] = filter_by_created_to
        if filter_by_created_by:
            params["filter[created_by][]"] = filter_by_created_by
        if filter_by_entity:
            params["filter[entity][]"] = filter_by_entity
        if filter_by_entity_id:
            params["filter[entity_id][]"] = filter_by_entity_id
        if filter_by_type:
            params["filter[type]"] = filter_by_type

        return f"{url}?{urlencode(params)}"

    def _build_get_event_url(
        self,
        id: int,
        with_params: list | None,
    ) -> str:
        url = f"{self.crm_url}/api/v4/events/{id}"
        params: dict = {}
        if with_params:
            params["with"] = ",".join(param for param in with_params)
        return f"{url}?{urlencode(params)}"

    def get_events_type(
        self,
        language_code: str | None = None,
    ) -> dict:
        """get events types
        Doc: https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#events-types
    
        Args:
            language_code (Optional[str], optional): language. Defaults to None.
    
        Returns:
            dict: {
                "_total_items": 35,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/events/types?limit=6"
                    }
                },
                "_embedded": {
                    "events_types": [
                        {
                            "key": "lead_added",
                            "type": 1,
                            "lang": "Новая сделка"
                        },
                        {
                            "key": "lead_deleted",
                            "type": 7,
                            "lang": "Сделка удалена"
                        },
                        ...
                    ]
                }
            }
        """
        url = self._build_get_events_type_url(language_code)
        return self._send_api_request("get", url)

    def get_events(
        self,
        page: int = 1,
        limit: int = 250,
        with_params: list | None = None,
        filter_by_ids: str | list | None = None,
        filter_by_created_from: str | list | None = None,
        filter_by_created_to: str | list | None = None,
        filter_by_created_by: str | list | None = None,
        filter_by_entity: str | list | None = None,
        filter_by_entity_id: str | list | None = None,
        filter_by_type: str | list | None = None,
    ) -> dict:
        """Get events
        Doc: https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#events-list
        Args:
            page (int, optional): page number. Defaults to 1.
            limit (int, optional): limit per page. Defaults to 250.
            with_params (Optional[list], optional): with params in doc. Defaults to None.
            filter_by_ids (Union[str, list, None], optional): ids filter. Defaults to None.
            filter_by_created_from (Union[str, list, None], optional): createdfrom. Defaults to None.
            filter_by_created_to (Union[str, list, None], optional): created to. Defaults to None.
            filter_by_created_by (Union[str, list, None], optional): created by. Defaults to None.
            filter_by_entity (Union[str, list, None], optional): by entity. Defaults to None.
            filter_by_entity_id (Union[str, list, None], optional): by entity_id. Defaults to None.
            filter_by_type (Union[str, list, None], optional): by type. Defaults to None.
    
        Returns:
            dict: {
                "_page": 1,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/events?limit=1&page=1"
                    },
                    "next": {
                        "href": "https://example.amocrm.ru/api/v4/events?limit=1&page=2"
                    }
                },
                "_embedded": {
                    "events": [
                        {
                            "id": "01pz58t6p04ymgsgfbmfyfy1mf",
                            "type": "lead_added",
                            "entity_id": 26060763,
                            "entity_type": "lead",
                            "created_by": 939801,
                            "created_at": 1888888888,
                            "value_after": [
                                {
                                    "note": {
                                        "id": 42743871
                                    }
                                }
                            ],
                            "value_before": [],
                            "account_id": 17079858,
                            "_links": {
                                "self": {
                                    "href": https://example.amocrm.ru/api/v4/events/01pz58t6p04ymgsgfbmfyfy1mf"
                                }
                            },
                            "_embedded": {
                                "entity": {
                                    "id": 26060763,
                                    "_links": {
                                        "self": {
                                            "href": "https://example.amocrm.ru/api/v4/leads/26060763"
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = self._build_get_events_url(
            page,
            limit,
            with_params,
            filter_by_ids,
            filter_by_created_from,
            filter_by_created_to,
            filter_by_created_by,
            filter_by_entity,
            filter_by_entity_id,
            filter_by_type,
        )
        return self._send_api_request("get", url)

    async def get_events_type_async(
        self,
        language_code: str | None = None,
    ) -> dict:
        """Async version of get_events_type."""
        url = self._build_get_events_type_url(language_code)
        return await self._send_api_request_async("get", url)

    async def get_events_async(
        self,
        page: int = 1,
        limit: int = 250,
        with_params: list | None = None,
        filter_by_ids: str | list | None = None,
        filter_by_created_from: str | list | None = None,
        filter_by_created_to: str | list | None = None,
        filter_by_created_by: str | list | None = None,
        filter_by_entity: str | list | None = None,
        filter_by_entity_id: str | list | None = None,
        filter_by_type: str | list | None = None,
    ) -> dict:
        """Async version of get_events."""
        url = self._build_get_events_url(
            page,
            limit,
            with_params,
            filter_by_ids,
            filter_by_created_from,
            filter_by_created_to,
            filter_by_created_by,
            filter_by_entity,
            filter_by_entity_id,
            filter_by_type,
        )
        return await self._send_api_request_async("get", url)

    async def get_event_async(
        self,
        id: int,
        with_params: list | None = None,
    ) -> dict:
        """Async version of get_event."""
        url = self._build_get_event_url(id, with_params)
        return await self._send_api_request_async("get", url)

    def get_event(
        self,
        id: int,
        with_params: list | None = None,
    ) -> dict:
        """Get event
        Doc: https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#events-detail
        Args:
            id (int): event id.
            with_params (Optional[list], optional): with params(check dock). Defaults to None.
        Returns: {
                "id": "01pz58t6p04ymgsgfbmfyfy1mf",
                "type": "lead_added",
                "entity_id": 26060763,
                "entity_type": "lead",
                "created_by": 939801,
                "created_at": 1888888888,
                "value_after": [
                    {
                        "note": {
                            "id": 42743871
                        }
                    }
                ],
                "value_before": [],
                "account_id": 17079858,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/events/01pz58t6p04ymgsgfbmfyfy1mf"
                    }
                },
                "_embedded": {
                    "entity": {
                        "id": 26060763,
                        "_links": {
                            "self": {
                                "href": "https://example.amocrm.ru/api/v4/leads/26060763"
                            }
                        }
                    }
                }
            }
        """
        url = self._build_get_event_url(id, with_params)
        return self._send_api_request("get", url)
