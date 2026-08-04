from .base import Entity

from typing import Optional, Union
from urllib.parse import urlencode

class Events(Entity):
    def get_events_type(
        self,
        language_code: Optional[str] = None,
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
        params = {"language_code": language_code}
        url = f"{self.crm_url}/api/v4/events/types?{urlencode(params)}"
        return self._send_api_request("get", url)

    def get_events(
        self,
        page: int = 1,
        limit: int = 250,
        with_params: Optional[list] = None,
        filter_by_ids: Union[str, list, None] = None,
        filter_by_created_from: Union[str, list, None] = None,
        filter_by_created_to: Union[str, list, None] = None,
        filter_by_created_by: Union[str, list, None] = None,
        filter_by_entity: Union[str, list, None] = None,
        filter_by_entity_id: Union[str, list, None] = None,
        filter_by_type: Union[str, list, None] = None,
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
        url = f"{self.crm_url}/api/v4/events"
        params: dict = {"limit": limit, "page": page}
        if with_params:
            params["with"] = ",".join(param for param in with_params)  # type: ignore
        if filter_by_ids:
            params["filter[id]"] = filter_by_ids  # type: ignore
        if filter_by_created_from:
            params["filter[created_at][from]"] = filter_by_created_from  # type: ignore
        if filter_by_created_to:
            params["filter[created_at][to]"] = filter_by_created_to  # type: ignore
        if filter_by_created_by:
            params["filter[created_by][]"] = filter_by_created_by  # type: ignore
        if filter_by_entity:
            params["filter[entity][]"] = filter_by_entity  # type: ignore
        if filter_by_entity_id:
            params["filter[entity_id][]"] = filter_by_entity_id  # type: ignore
        if filter_by_type:
            params["filter[type]"] = filter_by_type  # type: ignore
    
        url = f"{url}?{urlencode(params)}"
        return self._send_api_request("get", url)

    def get_event(
        self,
        id: int,
        with_params: Optional[list] = None,
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
        url = f"{self.crm_url}/api/v4/events/{id}"
        params = {}
        if with_params:
            params["with"] = ",".join(param for param in with_params)
    
        url = f"{url}?{urlencode(params)}"
        return self._send_api_request("get", url)
