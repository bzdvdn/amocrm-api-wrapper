from .base import Entity

from typing import Optional, Union
from urllib.parse import urlencode

class Unsorted(Entity):
    def _build_get_unsorted_leads_url(
        self,
        page: int,
        limit: int,
        filter_by_uids: Union[str, list, None],
        filter_by_pipeline_id: Union[str, list, None],
        filter_by_category: Union[str, list, None],
        order_by: Optional[dict],
    ) -> str:
        url = f"{self.crm_url}/api/v4/leads/unsorted"
        params: dict = {"limit": limit, "page": page}
        orders = {}
        if filter_by_uids:
            params["filter[uid]"] = filter_by_uids  # type: ignore
        if filter_by_category:
            params["filter[category]"] = filter_by_category  # type: ignore
        if filter_by_pipeline_id:
            params["filter[pipeline_id]"] = filter_by_pipeline_id  # type: ignore
        if order_by:
            orders = {f"order[{key}]": value for key, value in order_by.items()}
        url = f"{url}?{urlencode(params)}"
        if orders:
            url = f"{url}&{urlencode(orders)}"
        return url

    def _build_create_unsorted_params(
        self,
        source_uid: str,
        source_name: str,
        metadata: dict,
        contact: dict,
        lead: dict,
        comapany: dict,
        pipeline_id: Optional[int],
        created_at: Optional[int],
        request_id: Optional[str],
    ) -> dict:
        params: dict = {
            "source_uid": source_uid,
            "source_name": source_name,
            "metadata": metadata,
            "contact": contact,
        }
        _embedded = {"contacts": [contact], "leads": [lead], "companies": [comapany]}
        params["_embedded"] = _embedded
        if request_id:
            params["request_id"] = request_id
        if pipeline_id:
            params["pipeline_id"] = pipeline_id  # type: ignore
        if created_at:
            params["created_at"] = created_at  # type: ignore
        return params

    def _build_accept_unsorted_params(
        self,
        user_id: int,
        status_id: int,
    ) -> dict:
        return {"user_id": user_id, "status_id": status_id}

    def _build_get_summary_unsorted_url(
        self,
        uid: Union[str, list, None],
        created_at__from: Optional[str],
        created_at__to: Optional[str],
        pipeline_id: Union[str, list, None],
    ) -> str:
        params: dict = {}
        if uid:
            params["filter[uid]"] = uid
        if created_at__from:
            params["filter[created_at][from]"] = created_at__from
        if created_at__to:
            params["filter[created_at][to]"] = created_at__to
        if pipeline_id:
            params["filter[pipeline_id]"] = pipeline_id
        return f"{self.crm_url}/api/v4/leads/unsorted/summary?{urlencode(params)}"

    def get_unsorted_leads(
        self,
        page: int = 1,
        limit: int = 250,
        filter_by_uids: Union[str, list, None] = None,
        filter_by_pipeline_id: Union[str, list, None] = None,
        filter_by_category: Union[str, list, None] = None,
        order_by: Optional[dict] = None,
    ) -> dict:
        """get unsorted leads
        Doc: https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-list
        Args:
            page (int, optional): number of page. Defaults to 1.
            limit (int, optional): limit rows. Defaults to 250.
            filter_by_uids (Union[str, list, None], optional): filter by uids, values str or list. Defaults to None.
            filter_by_pipeline_id (Union[str, list, None], optional): filter by pipelines. Defaults to None.
            filter_by_category (Union[str, list, None], optional): filter by category(sip, mail, forms, chats). Defaults to None.
            order_by (Optional[dict], optional): orber by params like {'created_at': 'asc'}. Defaults to None.
    
        Returns:
            dict: {
                "_page": 1,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/unsorted?filter[uid]=98fb033cefde74f5de1a5d3980a2a2d108037"
                    }
                },
                "_embedded": {
                    "unsorted": [
                        {
                            "uid": "98fb033cefde74f5de1a5d3980a2a2d108037",
                            "source_uid": null,
                            "source_name": "UIS",
                            "category": "sip",
                            "pipeline_id": 2194576,
                            "created_at": 1583156937,
                            "metadata": {
                                "from": "7999999999",
                                "phone": 7999999999,
                                "called_at": 1583156916,
                                "duration": "0",
                                "link": null,
                                "service_code": "uis_widget"
                            },
                            "account_id": 123312,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/unsorted/98fb033cefde74f5de1a5d3980a2a2d108037"
                                }
                            },
                            "_embedded": {
                                "contacts": [
                                    {
                                        "id": 13176707,
                                        "_links": {
                                            "self": {
                                                "href": "https://example.amocrm.ru/api/v4/contacts/13176707"
                                            }
                                        }
                                    }
                                ],
                                "leads": [
                                    {
                                        "id": 7002787,
                                        "_links": {
                                            "self": {
                                                "href": "https://example.amocrm.ru/api/v4/leads/7002787"
                                            }
                                        }
                                    }
                                ],
                                "companies": []
                            }
                        }
                    ]
                }
            }
        """
        url = self._build_get_unsorted_leads_url(
            page, limit, filter_by_uids, filter_by_pipeline_id, filter_by_category, order_by
        )
        return self._send_api_request("get", url)

    def get_unsorted_by_uid(self, uid: str) -> dict:
        """Get unsorted obj by uid
        Doc: https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-detail
        Args:
            uid (str): uid
    
        Returns:
            dict: {
                "uid": "aa401affb0094076b7449008363c1dc77d6790ad13fb5b08176dc46daa18",
                "source_uid": "my_unique_uid",
                "source_name": "Название источника",
                "category": "forms",
                "pipeline_id": 3166396,
                "created_at": 1588840852,
                "metadata": {
                    "form_id": "my_best_form",
                    "form_name": "Обратная связь",
                    "form_page": "https://example.com/form",
                    "ip": "192.168.0.1",
                    "form_sent_at": "1570178452",
                    "referer": "https://google.com/search",
                    "visitor_uid": null
                },
                "account_id": 28805383,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/unsorted/aa401affb0094076b7449008363c1dc77d6790ad13fb5b08176dc46daa18"
                    }
                },
                "_embedded": {
                    "contacts": [
                        {
                            "id": 9567221,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/contacts/9567221"
                                }
                            }
                        }
                    ],
                    "leads": [
                        {
                            "id": 6414851,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/6414851"
                                }
                            }
                        }
                    ],
                    "companies": []
                }
            }
        """
        url = f"{self.crm_url}/api/v4/leads/unsorted/{uid}"
        return self._send_api_request("get", url)

    def _create_unsorted(
        self,
        entity: str,
        source_uid: str,
        source_name: str,
        metadata: dict,
        contact: dict,
        lead: dict,
        comapany: dict,
        pipeline_id: Optional[int] = None,
        created_at: Optional[int] = None,
        request_id: Optional[str] = None,
    ) -> dict:
        """create unsorted
    
        Args:
            entity (str): form or sip
            source_uid (str): unique uid
            source_name (str): name of unsorted object
            metadata (dict): meta object
            contact (dict): contact object
            lead (dict): lead object
            comapany (dict): company object
            pipeline_id (Optional[int], optional): id of pipeline. Defaults to None.
            created_at (Optional[int], optional): tamstamp of lead created. Defaults to None.
            request_id (Optional[str], optional): str. Defaults to None.
    
        Returns:
            dict: {
            "_total_items": 1,
            "_embedded": {
                "unsorted": [
                    {
                        "uid": "aa401affb0094076b74442bc3f401d53e103f264d6668fd3ecfd5acef42f",
                        "account_id": 28805383,
                        "request_id": "123",
                        "_links": {
                            "self": {
                                "href": "https://example.amocrm.ru/api/v4/leads/unsorted/aa401affb0094076b74442bc3f401d53e103f264d6668fd3ecfd5acef42f"
                            }
                        },
                        "_embedded": {
                            "contacts": [
                                {
                                    "id": 11075541,
                                    "_links": {
                                        "self": {
                                            "href": "https://example.amocrm.ru/api/v4/contacts/11075541"
                                        }
                                    }
                                }
                            ],
                            "leads": [
                                {
                                    "id": 7706509,
                                    "_links": {
                                        "self": {
                                            "href": "https://example.amocrm.ru/api/v4/leads/7706509"
                                        }
                                    }
                                }
                            ],
                            "companies": []
                        }
                    }
                ]
            }
        }
        """
        url = f"{self.crm_url}/api/v4/leads/unsorted/{entity}"
        params = self._build_create_unsorted_params(
            source_uid,
            source_name,
            metadata,
            contact,
            lead,
            comapany,
            pipeline_id,
            created_at,
            request_id,
        )
        return self._send_api_request("post", url, [params])

    def create_unsorted_by_sip(
        self,
        source_uid: str,
        source_name: str,
        metadata: dict,
        contact: dict,
        lead: dict,
        comapany: dict,
        pipeline_id: Optional[int] = None,
        created_at: Optional[int] = None,
        request_id: Optional[str] = None,
    ) -> dict:
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-add-sip
        """
        params: dict = {k: v for k, v in locals().items() if k != "self"}
        return self._create_unsorted(entity="sip", **params)

    def create_unsorted_by_form(
        self,
        source_uid: str,
        source_name: str,
        metadata: dict,
        contact: dict,
        lead: dict,
        comapany: dict,
        pipeline_id: Optional[int] = None,
        created_at: Optional[int] = None,
        request_id: Optional[str] = None,
    ) -> dict:
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-add-form
        """
        params: dict = {k: v for k, v in locals().items() if k != "self"}
        return self._create_unsorted(entity="form", **params)

    def accept_unsorted(self, uid: str, user_id: int, status_id: int) -> dict:
        """Accept unsorted
        Doc: https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-accept
        Args:
            uid (str): unsorted obejct uid
            user_id (int): user id
            status_id (int): status id
    
        Returns:
            dict: {
                "uid": "3cvd1de2ebfsd152fd6a465cd3e586cbdba6827",
                "pipeline_id": 31634,
                "category": "mail",
                "created_at": 1589165593,
                "_embedded": {
                    "leads": [
                        {
                            "id": 9944789,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/9944789"
                                }
                            }
                        }
                    ],
                    "contacts": [
                        {
                            "id": 16522451,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/contacts/16522451"
                                }
                            }
                        }
                    ],
                    "companies": []
                }
            }
        """
        url = f"{self.crm_url}/api/v4/leads/unsorted/{uid}/accept"
        params = self._build_accept_unsorted_params(user_id, status_id)
        return self._send_api_request("post", url, params)

    def decline_unsorted(self, uid: str, user_id: int) -> dict:
        """Decline unsorted
        Doc: https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-decline
        Args:
            uid (str): unsorted object uid
            user_id (int): user id
    
        Returns:
            dict: {
                "uid": "98bc1d1de2f960a2ad0e34b52823",
                "pipeline_id": 1394576,
                "category": "mail",
                "created_at": 1589115506,
                "_embedded": {
                    "leads": [
                        {
                            "id": 9937533,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/9937533"
                                }
                            }
                        }
                    ],
                    "contacts": [
                        {
                            "id": 163141,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/contacts/163141"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = f"{self.crm_url}/api/v4/leads/unsorted/{uid}/decline"
        params = {"user_id": user_id}
        return self._send_api_request("delete", url, params)

    def link_unsorted(self, uid: str, user_id: int, link: dict) -> dict:
        """Link unsorted to another entity
        Doc: https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-link
        Args:
            uid (str): unsorted object uid
            user_id (int): user id
            link (dict): link object like {'entity_id': 123, 'entity_type': 'leads'}
    
        Returns:
            dict: {
                "uid": "d7faa21ce091fe0da05d8d4c2075090c1e9bfd4",
                "_embedded": {
                    "leads": [
                        {
                            "id": 93144801,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/93144801"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = f"{self.crm_url}api/v4/leads/unsorted/{uid}/link"
        params = {"user_id": user_id, "link": link}
        return self._send_api_request("post", url, params)

    def get_summary_unsorted(
        self,
        uid: Union[str, list, None] = None,
        created_at__from: Optional[str] = None,
        created_at__to: Optional[str] = None,
        pipeline_id: Union[str, list, None] = None,
    ) -> dict:
        """Get summarty unsorted object
        Doc: https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-summary
        Args:
            uid (Union[str, list, None], optional): list or str uids. Defaults to None.
            created_at__from (Optional[str], optional): timestamp. Defaults to None.
            created_at__to (Optional[str]], optional): timestamp. Defaults to None.
            pipeline_id (Union[str, list, None], optional): int. Defaults to None.
    
        Returns:
            dict: {
                "total": 168,
                "accepted": 6,
                "declined": 2,
                "average_sort_time": 34521,
                "categories": {
                    "sip": {
                        "total": 31
                    },
                    "mail": {
                        "total": 41
                    },
                    "forms": {
                        "total": 27
                    },
                    "chats": {
                        "total": 69
                    }
                }
            }
        """
        url = self._build_get_summary_unsorted_url(
            uid, created_at__from, created_at__to, pipeline_id
        )
        return self._send_api_request("get", url)

    async def get_unsorted_leads_async(
        self,
        page: int = 1,
        limit: int = 250,
        filter_by_uids: Union[str, list, None] = None,
        filter_by_pipeline_id: Union[str, list, None] = None,
        filter_by_category: Union[str, list, None] = None,
        order_by: Optional[dict] = None,
    ) -> dict:
        """Async version of get_unsorted_leads."""
        url = self._build_get_unsorted_leads_url(
            page, limit, filter_by_uids, filter_by_pipeline_id, filter_by_category, order_by
        )
        return await self._send_api_request_async("get", url)

    async def get_unsorted_by_uid_async(self, uid: str) -> dict:
        """Async version of get_unsorted_by_uid."""
        url = f"{self.crm_url}/api/v4/leads/unsorted/{uid}"
        return await self._send_api_request_async("get", url)

    async def _create_unsorted_async(
        self,
        entity: str,
        source_uid: str,
        source_name: str,
        metadata: dict,
        contact: dict,
        lead: dict,
        comapany: dict,
        pipeline_id: Optional[int] = None,
        created_at: Optional[int] = None,
        request_id: Optional[str] = None,
    ) -> dict:
        """Async version of _create_unsorted."""
        url = f"{self.crm_url}/api/v4/leads/unsorted/{entity}"
        params = self._build_create_unsorted_params(
            source_uid,
            source_name,
            metadata,
            contact,
            lead,
            comapany,
            pipeline_id,
            created_at,
            request_id,
        )
        return await self._send_api_request_async("post", url, [params])

    async def create_unsorted_by_sip_async(
        self,
        source_uid: str,
        source_name: str,
        metadata: dict,
        contact: dict,
        lead: dict,
        comapany: dict,
        pipeline_id: Optional[int] = None,
        created_at: Optional[int] = None,
        request_id: Optional[str] = None,
    ) -> dict:
        """Async version of create_unsorted_by_sip."""
        params: dict = {k: v for k, v in locals().items() if k != "self"}
        return await self._create_unsorted_async(entity="sip", **params)

    async def create_unsorted_by_form_async(
        self,
        source_uid: str,
        source_name: str,
        metadata: dict,
        contact: dict,
        lead: dict,
        comapany: dict,
        pipeline_id: Optional[int] = None,
        created_at: Optional[int] = None,
        request_id: Optional[str] = None,
    ) -> dict:
        """Async version of create_unsorted_by_form."""
        params: dict = {k: v for k, v in locals().items() if k != "self"}
        return await self._create_unsorted_async(entity="form", **params)

    async def accept_unsorted_async(
        self, uid: str, user_id: int, status_id: int
    ) -> dict:
        """Async version of accept_unsorted."""
        url = f"{self.crm_url}/api/v4/leads/unsorted/{uid}/accept"
        params = self._build_accept_unsorted_params(user_id, status_id)
        return await self._send_api_request_async("post", url, params)

    async def decline_unsorted_async(self, uid: str, user_id: int) -> dict:
        """Async version of decline_unsorted."""
        url = f"{self.crm_url}/api/v4/leads/unsorted/{uid}/decline"
        params = {"user_id": user_id}
        return await self._send_api_request_async("delete", url, params)

    async def link_unsorted_async(self, uid: str, user_id: int, link: dict) -> dict:
        """Async version of link_unsorted."""
        url = f"{self.crm_url}api/v4/leads/unsorted/{uid}/link"
        params = {"user_id": user_id, "link": link}
        return await self._send_api_request_async("post", url, params)

    async def get_summary_unsorted_async(
        self,
        uid: Union[str, list, None] = None,
        created_at__from: Optional[str] = None,
        created_at__to: Optional[str] = None,
        pipeline_id: Union[str, list, None] = None,
    ) -> dict:
        """Async version of get_summary_unsorted."""
        url = self._build_get_summary_unsorted_url(
            uid, created_at__from, created_at__to, pipeline_id
        )
        return await self._send_api_request_async("get", url)
