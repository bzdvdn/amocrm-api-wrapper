from json import JSONDecodeError
from requests import Session, ConnectionError, ConnectTimeout
from typing import Optional, Union
from urllib.parse import urlencode

from .errors import AmoException


class BaseClient(object):
    def _init_session(self, headers: Optional[dict] = None) -> Session:
        raise NotImplementedError()

    def update_session_params(self, params: dict) -> None:
        """update session

        Args:
            params (dict): like {'IF-MODIFIED-SINCE': <datetime>}
        """
        self.session = self._init_session(params)

    def _send_api_request(
        self, method: str, url: str, data: Optional[dict] = None
    ) -> dict:
        try:
            response = self.session.__getattribute__(method)(url, json=data)
            if response.status_code == 204:
                return {}
            data = response.json()
            json_data = data['response'] if 'response' in data else data
            if 'error' in json_data:
                raise AmoException(json_data)
            return json_data
        except (ConnectTimeout, ConnectionError, JSONDecodeError) as e:
            raise AmoException({'error': str(e)})

    def _get_entities(
        self,
        entity: str,
        limit: int = 250,
        page: int = 1,
        with_params: Optional[list] = None,
        filters: Optional[dict] = None,
        order: Optional[dict] = None,
    ) -> dict:
        url = f'{self.crm_url}/api/v4/{entity}'
        params = {'limit': limit, 'page': page}
        if with_params:
            params['with'] = ','.join(param for param in with_params)
        if filters:
            filter_query = {f'filter[{k}]': v for k, v in filters.items()}
            params.update(filter_query)
        if order:
            order_query = {f'order[k]': v for k, v in order.items()}
            params.update(order_query)
        url = f'{url}?{urlencode(params)}'
        return self._send_api_request('get', url)

    def _get_entity_links(
        self, entity: str, entity_id: int, filters: Optional[dict] = None
    ) -> dict:
        url = f'{self.crm_url}/api/v4/{entity}/{entity_id}/links'
        if filters:
            filter_query = {f'filter[{k}]': v for k, v in filters.items()}
            url = f'{url}?{urlencode(filter_query)}'
        return self._send_api_request('get', url)

    def _link_entities(self, entity: str, entity_id: int, objects: list) -> dict:
        url = f'{self.crm_url}/api/v4/{entity}/{entity_id}/links'
        return self._send_api_request('post', url, objects)

    def _unlink_entities(self, entity: str, entity_id: int, objects: list) -> dict:
        url = f'{self.crm_url}/api/v4/{entity}/{entity_id}/unlinks'
        return self._send_api_request('post', url, objects)

    def unlink_leads_entity(self, entity_id: int, objects: list) -> dict:
        return self._unlink_entities('leads', entity_id, objects)

    def unlink_contacts_entity(self, entity_id: int, objects: list) -> dict:
        return self._unlink_entities('contacts', entity_id, objects)

    def unlink_customers_entity(self, entity_id: int, objects: list) -> dict:
        return self._unlink_entities('customers', entity_id, objects)

    def unlink_companies_entity(self, entity_id: int, objects: list) -> dict:
        return self._unlink_entities('companies', entity_id, objects)

    def link_leads_entity(self, entity_id: int, objects: list) -> dict:
        return self._link_entities('leads', entity_id, objects)
    
    def link_contacts_entity(self, entity_id: int, objects: list) -> dict:
        return self._link_entities('contcats', entity_id, objects)

    def link_companies_entity(self, entity_id: int, objects: list) -> dict:
        return self._link_entities('companies', entity_id, objects)

    def link_customers_entity(self, entity_id: int, objects: list) -> dict:
        return self._link_entities('customers', entity_id, objects)

    def get_leads_links(self, entity_id: int, filters: Optional[dict] = None) -> dict:
        return self._get_entity_links('leads', entity_id, filters)

    def get_contacts_links(
        self, entity_id: int, filters: Optional[dict] = None
    ) -> dict:
        return self._get_entity_links('contacts', entity_id, filters)

    def get_companies_links(
        self, entity_id: int, filters: Optional[dict] = None
    ) -> dict:
        return self._get_entity_links('companies', entity_id, filters)

    def get_customers_links(
        self, entity_id: int, filters: Optional[dict] = None
    ) -> dict:
        return self._get_entity_links('customers', entity_id, filters)

    def get_account_info(
        self,
        with_amojo_id: bool = False,
        with_amojo_rights: bool = False,
        with_users_groups: bool = False,
        with_task_types: bool = False,
        with_version: bool = False,
        with_ventity_names: bool = False,
        with_datetime_settings: bool = False,
    ) -> dict:
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/account-info    
        Args:
            with_amojo_id (bool, optional): . Defaults to False.
            with_amojo_rights (bool, optional): . Defaults to False.
            with_users_groups (bool, optional): . Defaults to False.
            with_task_types (bool, optional):. Defaults to False.
            with_version (bool, optional): . Defaults to False.
            with_ventity_names (bool, optional):. Defaults to False.
            with_datetime_settings (bool, optional):. Defaults to False.

        Returns:
            dict: query result
        """
        params = {k.replace('with_', ''): v for k, v in locals().items() if k != 'self'}
        with_params = [param for param, value in params.items() if value]
        url = f'{self.crm_url}/api/v4/account'
        url += '?with=' + ','.join(p for p in with_params)
        return self._send_api_request('get', url)

    def _create_or_update_entities(
        self, entity: str, objects: list, update: bool = False
    ) -> dict:
        """method for create or update entities

        Args:
            entity (str): name of entities like 'leads'
            objects (list): list of obejcts
            update (bool): if True http method patch else post

        Returns:
            dict: query result
        """
        url = f'{self.crm_url}/api/v4/{entity}'
        http_method = 'patch' if update else 'post'
        return self._send_api_request(http_method, url, objects)

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
        return self._create_or_update_entities('leads', objects)

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
        return self._create_or_update_entities('leads', objects, True)

    def get_lead(self, lead_id: int) -> dict:
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
        url = f'{self.crm_url}/api/v4/leads/{lead_id}'
        return self._send_api_request('get', url)

    def get_leads(
        self,
        limit: int = 250,
        page: int = 1,
        with_params: Optional[list] = None,
        filters: Optional[dict] = None,
        order: Optional[dict] = None,
    ) -> dict:
        """Get leads

        Args:
            limit (int, optional): limit of rows. Defaults to 250.
            page (int, optional): number of page. Defaults to 1.
            with_params (Optional[list], optional): params. Defaults to None.
            filters (Optional[dict], optional): filter params like {'[updated_at][from]': '<timestamp>'}. Defaults to None.
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
        params = {k: v for k, v in locals().items() if k != 'self'}
        return self._get_entities('leads', **params)

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
        url = f'{self.crm_url}/api/v4/unsorted'
        params = {'limit': limit, 'page': page}
        if filter_by_uids:
            params['filter[uid]'] = filter_by_uids
        if filter_by_category:
            params['filter[category]'] = filter_by_category
        if filter_by_pipeline_id:
            params['filter[pipeline_id]'] = filter_by_pipeline_id
        if order_by:
            orders = {f'order[{key}]': value for key, value in order_by.items()}
        url = f'{url}?{urlencode(params)}'
        return self._send_api_request('get', url)

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
        url = f'{self.crm_url}/api/v4/unsorted/{uid}'
        return self._send_api_request('get', url)

    def _create_unsorted(
        self,
        entity: str,
        source_uid: str,
        source_name: str,
        metadata: dict,
        conctact: dict,
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
            conctact (dict): contact object
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
        url = f'{self.crm}/api/v4/leads/unsorted/{entity}'
        params = {
            'source_uid': source_uid,
            'source_name': source_name,
            'metadata': metadata,
            'contact': conctact,
        }
        _embedded = {'contacts': [conctact], 'leads': [lead], 'companies': [comapany]}
        params['_embedded'] = _embedded
        if request_id:
            params['request_id'] = request_id
        if pipeline_id:
            params['pipeline_id'] = pipeline_id
        if created_at:
            params['created_at'] = created_at
        return self._send_api_request('post', url, [params])

    def create_unsorted_by_sip(
        self,
        source_uid: str,
        source_name: str,
        metadata: dict,
        conctact: dict,
        lead: dict,
        comapany: dict,
        pipeline_id: Optional[int] = None,
        created_at: Optional[int] = None,
        request_id: Optional[str] = None,
    ) -> dict:
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-add-sip
        """
        params = {k: v for k, v in locals() if k != 'self'}
        return self._create_unsorted(entity='sip', **params)

    def create_unsorted_by_form(
        self,
        source_uid: str,
        source_name: str,
        metadata: dict,
        conctact: dict,
        lead: dict,
        comapany: dict,
        pipeline_id: Optional[int] = None,
        created_at: Optional[int] = None,
        request_id: Optional[str] = None,
    ) -> dict:
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#unsorted-add-form
        """
        params = {k: v for k, v in locals().items() if k != 'self'}
        return self._create_unsorted(entity='form', **params)

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
        url = f'{self.crm_url}/api/v4/leads/unsorted/{uid}/accept'
        params = {'user_id': user_id, 'status_id': status_id}
        return self._send_api_request('post', url, params)

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
        url = f'{self.crm_url}/api/v4/leads/unsorted/{uid}/decline'
        params = {'user_id': user_id}
        return self._send_api_request('delete', url, params)

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
        url = f'{self.crm_url}api/v4/leads/unsorted/{uid}/link'
        params = {'user_id': user_id, 'link': link}
        return self._send_api_request('post', url, params)

    def get_summary_unsorted(
        self,
        uid: Union[str, list, None] = None,
        created_at__from: Union[str, list, None] = None,
        created_at__to: Union[str, list, None] = None,
        pipeline_id: Union[str, list, None] = None,
    ) -> dict:
        """Get summarty unsorted object

        Args:
            uid (Union[str, list, None], optional): list or str uids. Defaults to None.
            created_at__from (Union[str, list, None], optional): timestamp. Defaults to None.
            created_at__to (Union[str, list, None], optional): timestamp. Defaults to None.
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
        params = {}
        if uid:
            params['filter[uid]'] = uid
        if created_at__from:
            params['filter[created_at][from]'] = created_at__from
        if created_at__to:
            params['filter[created_at][to]'] = created_at__to
        if pipeline_id:
            params['filter[pipeline_id]'] = pipeline_id
        url = f'{url}?{urlencode(params)}'
        return self._send_api_request('get', url)

    def get_pipelines(self) -> dict:
        """get leads pipelines

        Returns:
            dict: {
                "_total_items": 1,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/pipelines"
                    }
                },
                "_embedded": {
                    "pipelines": [
                        {
                            "id": 3177727,
                            "name": "Воронка",
                            "sort": 1,
                            "is_main": true,
                            "is_unsorted_on": true,
                            "is_archive": false,
                            "account_id": 12345678,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727"
                                }
                            },
                            "_embedded": {
                                "statuses": [
                                    {
                                        "id": 32392156,
                                        "name": "Неразобранное",
                                        "sort": 10,
                                        "is_editable": false,
                                        "pipeline_id": 3177727,
                                        "color": "#c1c1c1",
                                        "type": 1,
                                        "account_id": 12345678,
                                        "_links": {
                                            "self": {
                                                "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392156"
                                            }
                                        }
                                    },
                                    {
                                        "id": 32392159,
                                        "name": "Первичный контакт",
                                        "sort": 20,
                                        "is_editable": true,
                                        "pipeline_id": 3177727,
                                        "color": "#99ccff",
                                        "type": 0,
                                        "account_id": 12345678,
                                        "_links": {
                                            "self": {
                                                "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392159"
                                            }
                                        }
                                    },
                                    {
                                        "id": 32392165,
                                        "name": "Принимают решение",
                                        "sort": 30,
                                        "is_editable": true,
                                        "pipeline_id": 3177727,
                                        "color": "#ffcc66",
                                        "type": 0,
                                        "account_id": 12345678,
                                        "_links": {
                                            "self": {
                                                "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392165"
                                            }
                                        }
                                    },
                                    {
                                        "id": 142,
                                        "name": "Успешно реализовано",
                                        "sort": 10000,
                                        "is_editable": false,
                                        "pipeline_id": 3177727,
                                        "color": "#CCFF66",
                                        "type": 0,
                                        "account_id": 12345678,
                                        "_links": {
                                            "self": {
                                                "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/142"
                                            }
                                        }
                                    },
                                    {
                                        "id": 143,
                                        "name": "Закрыто и не реализовано",
                                        "sort": 11000,
                                        "is_editable": false,
                                        "pipeline_id": 3177727,
                                        "color": "#D5D8DB",
                                        "type": 0,
                                        "account_id": 12345678,
                                        "_links": {
                                            "self": {
                                                "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/143"
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        """
        url = f'{self.crm_url}/api/v4/leads/pipelines'
        return self._send_api_request('get', url)

    def get_pipeline(self, pipeline_id: int) -> dict:
        """get leads pipeline

        Returns:
            dict: {
                "id": 3177727,
                "name": "Воронка",
                "sort": 1,
                "is_main": true,
                "is_unsorted_on": true,
                "is_archive": false,
                "account_id": 28847170,
                "_links": {
                    "self": {
                        "href": "https://shard152.amocrm.ru/api/v4/leads/pipelines/3177727"
                    }
                },
                "_embedded": {
                    "statuses": [
                        {
                            "id": 32392156,
                            "name": "Неразобранное",
                            "sort": 10,
                            "is_editable": false,
                            "pipeline_id": 3177727,
                            "color": "#c1c1c1",
                            "type": 1,
                            "account_id": 28847170,
                            "_links": {
                                "self": {
                                    "href": "https://shard152.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392156"
                                }
                            }
                        },
                        {
                            "id": 32392159,
                            "name": "Первичный контакт",
                            "sort": 20,
                            "is_editable": true,
                            "pipeline_id": 3177727,
                            "color": "#99ccff",
                            "type": 0,
                            "account_id": 28847170,
                            "_links": {
                                "self": {
                                    "href": "https://shard152.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392159"
                                }
                            }
                        },
                        {
                            "id": 32392165,
                            "name": "Принимают решение",
                            "sort": 30,
                            "is_editable": true,
                            "pipeline_id": 3177727,
                            "color": "#ffcc66",
                            "type": 0,
                            "account_id": 28847170,
                            "_links": {
                                "self": {
                                    "href": "https://shard152.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392165"
                                }
                            }
                        },
                        {
                            "id": 142,
                            "name": "Успешно реализовано",
                            "sort": 10000,
                            "is_editable": false,
                            "pipeline_id": 3177727,
                            "color": "#CCFF66",
                            "type": 0,
                            "account_id": 28847170,
                            "_links": {
                                "self": {
                                    "href": "https://shard152.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/142"
                                }
                            }
                        },
                        {
                            "id": 143,
                            "name": "Закрыто и не реализовано",
                            "sort": 11000,
                            "is_editable": false,
                            "pipeline_id": 3177727,
                            "color": "#D5D8DB",
                            "type": 0,
                            "account_id": 28847170,
                            "_links": {
                                "self": {
                                    "href": "https://shard152.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/143"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = f'{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}'
        return self._send_api_request('get', url)

    def create_pipeline(
        self,
        name: str,
        sort: int,
        is_main: bool,
        statuses: list,
        is_unsorted_on: bool = False,
        request_id: Optional[str] = None,
    ) -> dict:
        """craete pipeline
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipelines-add
        Args:
            name (str): name of pipeline
            sort (int): sort of pipeline
            is_main (bool): True or False, True if is main pipeline
            statuses (list): list of statuses objects
            is_unsorted_on (bool, optional): True if unsorted is enabled. Defaults to False.
            request_id (Optional[str], optional): random string for check request. Defaults to None.

        Returns:
            dict: query result
        """
        url = f'{self.crm_url}/api/v4/leads/pipelines'
        params = {
            'name': name,
            'sort': sort,
            'is_main': is_main,
            'statuses': statuses,
            'is_unsorted_on': is_unsorted_on,
        }
        if request_id:
            params['request_id'] = request_id
        return self._send_api_request('post', url, params)

    def edit_pipeline(
        self,
        pipeline_id: int,
        name: str,
        sort: int,
        is_main: bool,
        is_unsorted_on: bool,
    ) -> dict:
        """Edit pipeline
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipeline-edit
        Args:
            pipeline_id (int): id of pipeline
            name (str): name of pipeline
            sort (int):  sort of pipeline
            is_main (bool): True or False, True if is main pipeline
            is_unsorted_on (bool): True if unsorted is enabled

        Returns:
            dict: query result
        """
        url = f'{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}'
        params = {
            'name': name,
            'sort': sort,
            'is_main': is_main,
            'is_unsorted_on': is_unsorted_on,
        }
        return self._send_api_request('patch', url, params)

    def delete_pipeline(self, pipeline_id: int) -> dict:
        """Delete pipeline
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipeline-delete
        Args:
            pipeline_id (int): id of pipeline

        Returns:
            dict: query result
        """
        url = f'{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}'
        return self._send_api_request('delete', url)

    def get_pipeline_statuses(self, pipeline_id: int) -> dict:
        """return pipeline Statuses
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#statuses-list
        Args:
            pipeline_id (int): id of pipeline
        Returns:
            dict: {
            "_total_items": 1,
            "_links": {
                "self": {
                    "href": "https://example.amocrm.ru/api/v4/leads/pipelines"
                }
            },
            "_embedded": {
                "pipelines": [
                    {
                        "id": 3177727,
                        "name": "Воронка",
                        "sort": 1,
                        "is_main": true,
                        "is_unsorted_on": true,
                        "is_archive": false,
                        "account_id": 12345678,
                        "_links": {
                            "self": {
                                "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727"
                            }
                        },
                        "_embedded": {
                            "statuses": [
                                {
                                    "id": 32392156,
                                    "name": "Неразобранное",
                                    "sort": 10,
                                    "is_editable": false,
                                    "pipeline_id": 3177727,
                                    "color": "#c1c1c1",
                                    "type": 1,
                                    "account_id": 12345678,
                                    "_links": {
                                        "self": {
                                            "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392156"
                                        }
                                    }
                                },
                                {
                                    "id": 32392159,
                                    "name": "Первичный контакт",
                                    "sort": 20,
                                    "is_editable": true,
                                    "pipeline_id": 3177727,
                                    "color": "#99ccff",
                                    "type": 0,
                                    "account_id": 12345678,
                                    "_links": {
                                        "self": {
                                            "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392159"
                                        }
                                    }
                                },
                                {
                                    "id": 32392165,
                                    "name": "Принимают решение",
                                    "sort": 30,
                                    "is_editable": true,
                                    "pipeline_id": 3177727,
                                    "color": "#ffcc66",
                                    "type": 0,
                                    "account_id": 12345678,
                                    "_links": {
                                        "self": {
                                            "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392165"
                                        }
                                    }
                                },
                                {
                                    "id": 142,
                                    "name": "Успешно реализовано",
                                    "sort": 10000,
                                    "is_editable": false,
                                    "pipeline_id": 3177727,
                                    "color": "#CCFF66",
                                    "type": 0,
                                    "account_id": 12345678,
                                    "_links": {
                                        "self": {
                                            "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/142"
                                        }
                                    }
                                },
                                {
                                    "id": 143,
                                    "name": "Закрыто и не реализовано",
                                    "sort": 11000,
                                    "is_editable": false,
                                    "pipeline_id": 3177727,
                                    "color": "#D5D8DB",
                                    "type": 0,
                                    "account_id": 12345678,
                                    "_links": {
                                        "self": {
                                            "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/143"
                                        }
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
        """
        url = f'{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}/statuses'
        return self._send_api_request('get', url)

    def get_pipeline_status(self, pipeline_id: int, status_id: int) -> dict:
        """Get status
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#status-detail
        Args:
            pipeline_id (int): id of pipeline
            status_id (int): id of status

        Returns:
            dict: {
                "id": 32392156,
                "name": "Неразобранное",
                "sort": 10,
                "is_editable": false,
                "pipeline_id": 3177727,
                "color": "#c1c1c1",
                "type": 1,
                "account_id": 12345678,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392156"
                    }
                }
            }
        """
        url = (
            f'{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}/statuses/{status_id}'
        )
        return self._send_api_request('get', url)

    def add_statuses_to_pipeline(self, pipeline_id: int, statuses: list) -> dict:
        """Add status tot pipeline
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#statuses-add
        Args:
            pipeline_id (int): id of pipeline
            statuses (list): list of status object

        Returns:
            dict: {
                "_total_items": 2,
                "_embedded": {
                    "statuses": [
                        {
                            "id": 33035290,
                            "name": "Новый этап",
                            "sort": 60,
                            "is_editable": true,
                            "pipeline_id": 3270355,
                            "color": "#fffeb2",
                            "type": 0,
                            "account_id": 1415131,
                            "request_id": "0",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3270355/statuses/33035290"
                                }
                            }
                        },
                        {
                            "id": 33035293,
                            "name": "Новый этап 2",
                            "sort": 70,
                            "is_editable": true,
                            "pipeline_id": 3270355,
                            "color": "#fffeb2",
                            "type": 0,
                            "account_id": 1415131,
                            "request_id": "1",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3270355/statuses/33035293"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = f'{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}/statuses'
        return self._send_api_request('post', url, statuses)

    def edit_pipeline_status(
        self, pipeline_id: int, status_id: int, name: str, sort: int, color: str
    ) -> dict:
        """Edit pipeline status
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#status-edit
        Args:
            pipeline_id (int): id of pipeline
            status_id (int): id of status
            name (str): status name
            sort (int): sort of status
            color (str): status color

        Returns:
            dict: {
                "id": 32392165,
                "name": "Новое название для статуса",
                "sort": 20,
                "is_editable": true,
                "pipeline_id": 3177727,
                "color": "#c1e0ff",
                "type": 0,
                "account_id": 12345678,
                "request_id": "0",
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/pipelines/3177727/statuses/32392165"
                    }
                }
            }
        """
        url = (
            f'{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}/statuses/{status_id}'
        )
        params = {'name': name, 'sort': sort, 'color': color}
        return self._send_api_request('patch', url, params)

    def delete_status_from_pipeline(self, pipeline_id: int, status_id: int) -> dict:
        """Delete status from pipeline
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#status-delete
        Args:
            pipeline_id (int): id of pipeline
            status_id (int): id of status

        Returns:
            dict: {}
        """
        url = (
            f'{self.crm_url}/api/v4/leads/pipelines/{pipeline_id}/statuses/{status_id}'
        )
        return self._send_api_request('delete', url)

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
        params = {k: v for k, v in locals().items() if k != 'self'}
        return self._get_entities('contacts', **params)

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
        url = f'{self.crm_url}/api/v4/contacts/{contact_id}'
        return self._send_api_request('get', url)

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
        return self._create_or_update_entities('contacts', contacts)

    def update_conctacts(self, contacts: list) -> dict:
        """Update contcats

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
        url = f'{self.crm_url}/api/v4/contacts'
        return self._create_or_update_entities('contacts', contacts, True)

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
        params = {k: v for k, v in locals().items() if k != 'self'}
        return self._get_entities('companies', **params)

    def get_company(self, company_id: int) -> dict:
        """Get company

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
        url = f'{self.crm_url}/api/v4/companies/{company_id}'
        return self._send_api_request('get', url)

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
        url = f'{self.crm_url}/api/v4/companies'
        return self._send_api_request('post', companies)

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
        url = f'{self.crm_url}/api/v4/companies'
        return self._send_api_request('post', companies, True)

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
        params = {'page': page, 'limit': limit}
        return self._get_entities('catalogs', **params)

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
        url = f'{self.crm_url}/api/v4/catalogs/{catalog_id}'
        return self._send_api_request('get', url)

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
        return self._create_or_update_entities('catalogs', catalogs)

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
        return self._create_or_update_entities('catalogs', catalogs, True)

    def get_catalog_elements(
        self,
        catalog_id: int,
        page: int = 1,
        limit: int = 250,
        filters: Optional[dict] = None,
    ) -> dict:
        """Get elements by catalog id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/catalogs-api#list-elements-list
        Args:
            catalog_id (int): id of catalog
            page (int, optional): number of page. Defaults to 1.
            limit (int, optional): limit rows. Defaults to 250.
            filters (Optional[dict], optional): filter dict. Defaults to None.

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
        params = {'page': page, 'limit': limit, 'filters': filters}
        entity = f'catalogs/{catalog_id}/elements'
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
        url = f'{self.crm_url}/api/v4/catalogs/{catalog_id}/elements/{element_id}'
        return self._send_api_request('get', url)

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
            f'catalogs/{catalog_id}/elements', elements
        )

    def update_elements_to_catalog(self, catalog_id: int, elements: list) -> dict:
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
            f'catalogs/{catalog_id}/elements', elements, True
        )

    def _get_custom_fields(self, entity: str) -> dict:
        url = f'{self.crm_url}/api/v4/{entity}/custom_fields'
        return self._send_api_request('get', url)

    def get_contacts_custom_fields(self) -> dict:
        return self._get_custom_fields('contacts')

    def get_leads_custom_fields(self) -> dict:
        return self._get_custom_fields('leads')

    def get_companies_custom_fields(self) -> dict:
        return self._get_custom_fields('companies')

    def get_customers_custom_fields(self) -> dict:
        return self._get_custom_fields('customers')

    def get_customer_segments_custom_fields(self) -> dict:
        return self._get_custom_fields('customers/segments')

    def get_catalog_custom_fields(self, catalog_id: str) -> dict:
        return self._get_custom_fields(f'catalogs/{catalog_id}')

    def get_users(
        self,
        page: int = 1,
        limit_rows: int = 250,
        with_role: bool = False,
        with_group: bool = False,
    ) -> dict:
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/users-api#users-list
        :param page: int (number of page) 
        :param limit_rows: int (limit)
        :param with_role: bool
        :param with_group: bool
        :return: dict
        """
        url = f'{self.crm_url}/api/v4/users'
        params = {'page': page, 'limit_rows': limit_rows}
        with_ = []
        if with_group:
            with_.append('group')
        if with_role:
            with_.append('role')
        url = f'{url}?{urlencode(params)}'
        if with_:
            with_str = ','.join(i for i in with_)
            url = f'{url}&with={with_str}'
        return self._send_api_request('get', url)

    def get_user(
        self, user_id: int, with_role: bool = False, with_group: bool = False,
    ) -> dict:
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/users-api#user-detail
        :param user_id: int  
        :param with_role: bool
        :param with_group: bool
        :return: dict
        """
        url = f'{self.crm_url}/api/v4/users/{user_id}'
        with_ = []
        if with_group:
            with_.append('group')
        if with_role:
            with_.append('role')
        if with_:
            with_str = ','.join(i for i in with_)
            url = f'{url}?with={with_str}'
        return self._send_api_request('get', url)

    def get_webhooks(self) -> dict:
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/webhooks-api#webhooks-list
        """
        url = f'{self.crm_url}/api/v4/webhooks'
        return self._send_api_request('get', url)

    def subscribe_webhook(self, destination: str, settings: list) -> dict:
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/webhooks-api#webhooks-list
        :param destination: str (webhook url)  
        :param settings: list (list of events)
        :return: dict
        """
        url = f'{self.crm_url}/api/v4/webhooks'
        params = {'destination': destination, 'settings': settings}
        return self._send_api_request('post', url)

    def unsubscribe_webhook(self):
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/webhooks-api#webhooks-delete
        """
        url = f'{self.crm_url}/api/v4/webhooks'
        return self._send_api_request('delete', url)

    def get_widgets(self, page: int = 1, limit_rows: int = 250) -> dict:
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widgets-list
        :param page: int (page)  
        :param limit_rows: int 
        :return: dict
        """
        url = f'{self.crm_url}/api/v4/widgets'
        params = {'page': page, 'limit': limit_rows}
        url = f'{url}?{urlencode(params)}'
        return self._send_api_request('get', url)

    def get_widget(self, widget_code: str) -> dict:
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widget-detail
        :param widget_code: str
        :return: dict
        """
        url = f'{self.crm_url}/api/v4/widgets/{widget_code}'
        return self._send_api_request('get', url)

    def install_widget(self, widget_code: str, **kwargs) -> dict:
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widget-install
        :param widget_code: str (page)
        :return: dict
        """
        url = f'{self.crm_url}/api/v4/widgets/{widget_code}'
        return self._send_api_request('post', url, kwargs)

    def uninstall_widget(self, widget_code: str) -> dict:
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widget-uninstall
        :param widget_code: str (page)
        :return: dict
        """
        url = f'{self.crm_url}/api/v4/widgets/{widget_code}'
        return self._send_api_request('delete', url)
