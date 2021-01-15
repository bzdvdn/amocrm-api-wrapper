from json import JSONDecodeError, loads
from requests import Session, ConnectionError, ConnectTimeout, Response
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
        self._session = self._init_session(params)

    def _parse_response_body(self, response: Response) -> dict:
        raw_data = response.content.decode('utf-8')
        if not raw_data:
            return {}
        data = loads(raw_data)
        return data

    def _send_api_request(
        self, method: str, url: str, data: Optional[dict] = None
    ) -> dict:
        try:
            response = self._session.__getattribute__(method)(url, json=data)
            if response.status_code == 204:
                return {}
            data = self._parse_response_body(response)
            if 'error' in data or response.status_code >= 400:
                raise AmoException(data, code=response.status_code)
            json_data = data['response'] if 'response' in data else data
            return json_data
        except (ConnectTimeout, ConnectionError, JSONDecodeError) as e:
            raise AmoException({'error': str(e)}, code=500)

    def __create_filter_query(self, filters: dict) -> dict:
        filter_query = {}
        update_from = filters.pop('updated_at__from', None)
        update_to = filters.pop('updated_at__to', None)
        created_from = filters.pop('created_at__from', None)
        created_to = filters.pop('created_at__to', None)
        closed_from = filters.pop('closed_at__from', None)
        closed_to = filters.pop('closed_at__to', None)
        if update_from:
            filter_query['filter[updated_at][from]'] = update_from
        if update_to:
            filter_query['filter[updated_at][to]'] = update_to
        if created_from:
            filter_query['filter[created_at][from]'] = created_from
        if created_to:
            filter_query['filter[created_at][to]'] = created_to
        if closed_from:
            filter_query['filter[closed_at][from]'] = closed_from
        if closed_to:
            filter_query['filter[closed_at][to]'] = created_to
        filter_query.update({f'filter[{k}]': v for k, v in filters.items()})
        return filter_query

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
            filter_query = self.__create_filter_query(filters)
            params.update(filter_query)
        if order:
            order_query = {f'order[{k}]': v for k, v in order.items()}
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
        url = f'{self.crm_url}/api/v4/{entity}/{entity_id}/link'
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
        return self._link_entities('contacts', entity_id, objects)

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
            dict: {
                "id": 1231414,
                "name": "example",
                "subdomain": "example",
                "created_at": 1585840134,
                "created_by": 321321,
                "updated_at": 1589472711,
                "updated_by": 321321,
                "current_user_id": 581651,
                "country": "RU",
                "customers_mode": "segments",
                "is_unsorted_on": true,
                "is_loss_reason_enabled": true,
                "is_helpbot_enabled": false,
                "is_technical_account": false,
                "contact_name_display_order": 1,
                "amojo_id": "f3c6340d-410e-4ad1-9f7e-c5e663599909",
                "uuid": "824f3a59-6154-4edf-ba90-0b5593715d07",
                "version": 11,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/account"
                    }
                },
                "_embedded": {
                    "amojo_rights": {
                        "can_direct": true,
                        "can_create_groups": true
                    },
                    "users_groups": [
                        {
                            "id": 0,
                            "name": "Отдел продаж",
                            "uuid": null
                        }
                    ],
                    "task_types": [
                        {
                            "id": 1,
                            "name": "Связаться",
                            "color": null,
                            "icon_id": null,
                            "code": "FOLLOW_UP"
                        },
                        {
                            "id": 2,
                            "name": "Встреча",
                            "color": null,
                            "icon_id": null,
                            "code": "MEETING"
                        }
                    ],
                    "entity_names": {
                        "leads": {
                            "ru": {
                                "gender": "m",
                                "plural_form": {
                                    "dative": "клиентам",
                                    "default": "клиенты",
                                    "genitive": "клиентов",
                                    "accusative": "клиентов",
                                    "instrumental": "клиентами",
                                    "prepositional": "клиентах"
                                },
                                "singular_form": {
                                    "dative": "клиенту",
                                    "default": "клиент",
                                    "genitive": "клиента",
                                    "accusative": "клиента",
                                    "instrumental": "клиентом",
                                    "prepositional": "клиенте"
                                }
                            },
                            "en": {
                                "singular_form": {
                                    "default": "lead"
                                },
                                "plural_form": {
                                    "default": "leads"
                                },
                                "gender": "f"
                            },
                            "es": {
                                "singular_form": {
                                    "default": "acuerdo"
                                },
                                "plural_form": {
                                    "default": "acuerdos"
                                },
                                "gender": "m"
                            }
                        }
                    },
                    "datetime_settings": {
                        "date_pattern": "d.m.Y H:i",
                        "short_date_pattern": "d.m.Y",
                        "short_time_pattern": "H:i",
                        "date_formant": "d.m.Y",
                        "time_format": "H:i:s",
                        "timezone": "Europe/Moscow",
                        "timezone_offset": "+03:00"
                    }
                }
                }
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
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads-api#leads-list
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
        url = f'{self.crm}/api/v4/leads/unsorted/{entity}'
        params = {
            'source_uid': source_uid,
            'source_name': source_name,
            'metadata': metadata,
            'contact': contact,
        }
        _embedded = {'contacts': [contact], 'leads': [lead], 'companies': [comapany]}
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
        params = {k: v for k, v in locals() if k != 'self'}
        return self._create_unsorted(entity='sip', **params)

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
        params = {}
        if uid:
            params['filter[uid]'] = uid
        if created_at__from:
            params['filter[created_at][from]'] = created_at__from
        if created_at__to:
            params['filter[created_at][to]'] = created_at__to
        if pipeline_id:
            params['filter[pipeline_id]'] = pipeline_id
        url = f'{self.crm_url}/api/v4/leads/unsorted/summary?{urlencode(params)}'
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
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#pipelines-list
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
            '_embedded': {'statuses': statuses},
            'is_unsorted_on': is_unsorted_on,
        }
        if request_id:
            params['request_id'] = request_id
        return self._send_api_request('post', url, [params])

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
        limit: int = 250,
        with_role: bool = False,
        with_group: bool = False,
    ) -> dict:
        """Get users
        Doc: https://www.amocrm.ru/developers/content/crm_platform/users-api#users-list
        Args:
            page (int, optional): number of page. Defaults to 1.
            limit (int, optional): limit rows. Defaults to 250.
            with_role (bool, optional): return roles by user. Defaults to False.
            with_group (bool, optional): retur groups by user. Defaults to False.

        Returns:
            dict: {
                "_total_items": 2,
                "_page": 1,
                "_page_count": 1,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/users/?with=role,group"
                    }
                },
                "_embedded": {
                    "users": [
                        {
                            "id": 123123,
                            "name": "Пользователь для примера 2",
                            "email": "example2@mail.com",
                            "lang": "en",
                            "rights": {
                                "leads": {
                                    "view": "A",
                                    "edit": "A",
                                    "add": "A",
                                    "delete": "A",
                                    "export": "A"
                                },
                                "contacts": {
                                    "view": "A",
                                    "edit": "A",
                                    "add": "A",
                                    "delete": "A",
                                    "export": "A"
                                },
                                "companies": {
                                    "view": "A",
                                    "edit": "A",
                                    "add": "A",
                                    "delete": "A",
                                    "export": "A"
                                },
                                "tasks": {
                                    "edit": "A",
                                    "delete": "A"
                                },
                                "mail_access": false,
                                "catalog_access": false,
                                "status_rights": [
                                    {
                                        "entity_type": "leads",
                                        "pipeline_id": 2194576,
                                        "status_id": 30846277,
                                        "rights": {
                                            "view": "A",
                                            "edit": "A",
                                            "delete": "A"
                                        }
                                    },
                                    {
                                        "entity_type": "leads",
                                        "pipeline_id": 2212201,
                                        "status_id": 30965377,
                                        "rights": {
                                            "view": "A",
                                            "edit": "A",
                                            "delete": "A"
                                        }
                                    }
                                ],
                                "is_admin": false,
                                "is_free": false,
                                "is_active": true,
                                "group_id": null,
                                "role_id": null
                            },
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/users/123123/"
                                }
                            },
                            "_embedded": {
                            "roles": [
                                    {
                                        "id": 3141,
                                        "name": "Менеджер",
                                        "_links": {
                                            "self": {
                                                "href": "https://example.amocrm.ru/api/v4/roles/3141"
                                            }
                                        }
                                    }
                                ],
                                "groups": [
                                    {
                                        "id": 267688,
                                        "name": "Менеджеры"
                                    }
                                ]
                            }
                        },
                        {
                            "id": 321321,
                            "name": "Пользователь для примера 2",
                            "email": "example2@mail.com",
                            "lang": "ru",
                            "rights": {
                                "leads": {
                                    "view": "A",
                                    "edit": "A",
                                    "add": "G",
                                    "delete": "D",
                                    "export": "M"
                                },
                                "contacts": {
                                    "view": "A",
                                    "edit": "A",
                                    "add": "G",
                                    "delete": "M",
                                    "export": "D"
                                },
                                "companies": {
                                    "view": "A",
                                    "edit": "G",
                                    "add": "G",
                                    "delete": "D",
                                    "export": "D"
                                },
                                "tasks": {
                                    "edit": "A",
                                    "delete": "A"
                                },
                                "mail_access": true,
                                "catalog_access": true,
                                "status_rights": null,
                                "is_admin": true,
                                "is_free": false,
                                "is_active": true,
                                "group_id": null,
                                "role_id": null
                            },
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/users/321321"
                                }
                            },
                            "_embedded": {
                                "roles": [],
                                "groups": []
                            }
                        }
                    ]
                }
            }
        """
        url = f'{self.crm_url}/api/v4/users'
        params = {'page': page, 'limit': limit}
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
        """Get user
        Doc: https://www.amocrm.ru/developers/content/crm_platform/users-api#user-detail
        Args:
            user_id (int): id of user
            with_role (bool, optional): return roles. Defaults to False.
            with_group (bool, optional): return groups. Defaults to False.

        Returns:
            dict: {
                "id": 185848,
                "name": "Алексей Поимцев",
                "email": "test@example.com",
                "lang": "ru",
                "rights": {
                    "leads": {
                        "view": "M",
                        "edit": "M",
                        "add": "D",
                        "delete": "M",
                        "export": "M"
                    },
                    "contacts": {
                        "view": "M",
                        "edit": "M",
                        "add": "D",
                        "delete": "M",
                        "export": "M"
                    },
                    "companies": {
                        "view": "M",
                        "edit": "M",
                        "add": "D",
                        "delete": "M",
                        "export": "M"
                    },
                    "tasks": {
                        "edit": "A",
                        "delete": "A"
                    },
                    "mail_access": false,
                    "catalog_access": true,
                    "status_rights": [
                        {
                            "entity_type": "leads",
                            "pipeline_id": 3166396,
                            "status_id": 142,
                            "rights": {
                                "view": "D",
                                "edit": "D",
                                "delete": "D",
                                "export": "D"
                            }
                        },
                        {
                            "entity_type": "leads",
                            "pipeline_id": 3166396,
                            "status_id": 32311027,
                            "rights": {
                                "view": "D",
                                "edit": "D",
                                "delete": "D"
                            }
                        },
                        {
                            "entity_type": "leads",
                            "pipeline_id": 3104455,
                            "status_id": 31881115,
                            "rights": {
                                "view": "D",
                                "edit": "D",
                                "delete": "D"
                            }
                        }
                    ],
                    "is_admin": false,
                    "is_free": false,
                    "is_active": true,
                    "group_id": null,
                    "role_id": null
                },
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/users/185848"
                    }
                }
            }
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

    def get_webhooks(self, distansion: Optional[str] = None) -> dict:
        """Get webwooks
        Doc: https://www.amocrm.ru/developers/content/crm_platform/webhooks-api#webhooks-list
        Args:
            distansion (Optional[str], optional): filter by webhook url. Defaults to None.

        Returns:
            dict: {
                "_total_items": 2,
                "_embedded": {
                    "webhooks": [
                        {
                            "id": 839656,
                            "destination": "https://webhook-uri.com",
                            "created_at": 1575539157,
                            "updated_at": 1575539157,
                            "account_id": 321321,
                            "created_by": 123123,
                            "sort": 1,
                            "disabled": false,
                            "settings": [
                                "add_task"
                            ]
                        },
                        {
                            "id": 849193,
                            "destination": "https://api.test.ru/amoWebHook",
                            "created_at": 1576157524,
                            "updated_at": 1585816857,
                            "account_id": 321321,
                            "created_by": 123123,
                            "sort": 2,
                            "disabled": true,
                            "settings": [
                                "update_lead"
                            ]
                        }
                    ]
                }
            }
        """
        url = f'{self.crm_url}/api/v4/webhooks'
        if distansion:
            params = {'filter[distansion]': distansion}
            url = f'{url}?{urlencode(params)}'
        return self._send_api_request('get', url)

    def subscribe_webhook(self, destination: str, settings: list) -> dict:
        """Subscribe on webhook
        Doc: https://www.amocrm.ru/developers/content/crm_platform/webhooks-api#webhook-subscribe
        Args:
            destination (str): webhook url
            settings (list): webhook settings

        Returns:
            dict: {
                "id": 1056949,
                "destination": "https://example.test",
                "created_at": 1589012268,
                "updated_at": 1589012268,
                "account_id": 321321,
                "created_by": 3944275,
                "sort": 1,
                "disabled": false,
                "settings": [
                    "add_lead"
                ]
            }
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

    def get_widgets(self, page: int = 1, limit: int = 250) -> dict:
        """Get widgets
        Doc: https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widgets-list
        Args:
            page (int, optional): number of page. Defaults to 1.
            limit (int, optional): limit rows. Defaults to 250.

        Returns:
            dict: {
                "_page": 1,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/widgets?limit=2&page=1"
                    },
                    "next": {
                        "href": "https://example.amocrm.ru/api/v4/widgets?limit=2&page=2"
                    }
                },
                "_embedded": {
                    "widgets": [
                        {
                            "id": 742,
                            "code": "amo_dropbox",
                            "version": "0.0.13",
                            "rating": "2,8",
                            "settings_template": [
                                {
                                    "key": "conf",
                                    "name": "custom",
                                    "type": "custom",
                                    "is_required": false
                                }
                            ],
                            "is_lead_source": false,
                            "is_work_with_dp": false,
                            "is_crm_template": false,
                            "client_uuid": null,
                            "is_active_in_account": false,
                            "pipeline_id": null,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/widgets/amo_dropbox"
                                }
                            }
                        },
                        {
                            "id": 796,
                            "code": "amo_mailchimp",
                            "version": "1.1.12",
                            "rating": "3,4",
                            "settings_template": [
                                {
                                    "key": "api",
                                    "name": "custom",
                                    "type": "custom",
                                    "is_required": false
                                }
                            ],
                            "is_lead_source": false,
                            "is_work_with_dp": false,
                            "is_crm_template": false,
                            "client_uuid": null,
                            "is_active_in_account": false,
                            "pipeline_id": null,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/widgets/amo_mailchimp"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = f'{self.crm_url}/api/v4/widgets'
        params = {'page': page, 'limit': limit}
        url = f'{url}?{urlencode(params)}'
        return self._send_api_request('get', url)

    def get_widget(self, widget_code: str) -> dict:
        """Get widget
        Doc: https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widget-detail
        Args:
            widget_code (str): code of widget

        Returns:
            dict: {
                "id": 742,
                "code": "amo_dropbox",
                "version": "0.0.13",
                "rating": "2,8",
                "settings_template": [
                    {
                        "key": "conf",
                        "name": "custom",
                        "type": "custom",
                        "is_required": false
                    }
                ],
                "is_lead_source": false,
                "is_work_with_dp": false,
                "is_crm_template": false,
                "client_uuid": null,
                "is_active_in_account": false,
                "pipeline_id": null,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/widgets/amo_dropbox"
                    }
                }
            }
        """
        url = f'{self.crm_url}/api/v4/widgets/{widget_code}'
        return self._send_api_request('get', url)

    def install_widget(self, widget_code: str, **kwargs) -> dict:
        """Install widget
        Doc: https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widget-install
        Args:
            widget_code (str): widget code

        Returns:
            dict: {
                "id": 972,
                "code": "amo_asterisk",
                "version": "1.1.6",
                "rating": "2,7",
                "settings_template": [
                    {
                        "key": "login",
                        "name": "Логин",
                        "type": "text",
                        "is_required": true
                    },
                    {
                        "key": "password",
                        "name": "Пароль",
                        "type": "pass",
                        "is_required": true
                    },
                    {
                        "key": "phones",
                        "name": "Список телефонов",
                        "type": "users",
                        "is_required": true
                    },
                    {
                        "key": "script_path",
                        "name": "Путь к скрипту",
                        "type": "text",
                        "is_required": true
                    }
                ],
                "is_lead_source": false,
                "is_work_with_dp": false,
                "is_crm_template": false,
                "client_uuid": null,
                "is_active_in_account": true,
                "pipeline_id": null,
                "settings": {
                    "login": "example",
                    "password": "eXaMp1E",
                    "phones": {
                        "504141": "1039"
                    },
                    "script_path": "https://example.com/"
                },
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/widgets/amo_asterisk"
                    }
                }
            }
        """
        url = f'{self.crm_url}/api/v4/widgets/{widget_code}'
        return self._send_api_request('post', url, kwargs)

    def uninstall_widget(self, widget_code: str) -> dict:
        """Uninstall widget
        Doc: https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widget-uninstall
        Args:
            widget_code (str): code of widget

        Returns:
            dict: {}
        """

        url = f'{self.crm_url}/api/v4/widgets/{widget_code}'
        return self._send_api_request('delete', url)

    def get_tasks(
        self,
        page: int = 1,
        limit: int = 250,
        filters: Optional[dict] = None,
        order: Optional[dict] = None,
    ) -> dict:
        """Get tasks
        Doc: https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-list
        Args:
            page (int, optional): number of page. Defaults to 1.
            limit (int, optional): limit row. Defaults to 250.
            filters (Optional[dict], optional): {'[updated_at][from]': <timestamp>}. Defaults to None.
            order (Optional[dict], optional): {'updated_at': <timestamp>}. Defaults to None.

        Returns:
            dict: {
                "_page": 1,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/tasks?filter[task_type][]=2&filter[is_completed][]=1&limit=2&page=1"
                    },
                    "next": {
                        "href": "https://example.amocrm.ru/api/v4/tasks?filter[task_type][]=2&filter[is_completed][]=1&limit=2&page=2"
                    }
                },
                "_embedded": {
                    "tasks": [
                        {
                            "id": 7087,
                            "created_by": 3987910,
                            "updated_by": 3987910,
                            "created_at": 1575364000,
                            "updated_at": 1575364851,
                            "responsible_user_id": 123123,
                            "group_id": 0,
                            "entity_id": 167353,
                            "entity_type": "leads",
                            "duration": 0,
                            "is_completed": true,
                            "task_type_id": 2,
                            "text": "Пригласить на бесплатную тренировку",
                            "result": [],
                            "complete_till": 1575665940,
                            "account_id": 321321,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/tasks/7087"
                                }
                            }
                        },
                        {
                            "id": 215089,
                            "created_by": 0,
                            "updated_by": 3987910,
                            "created_at": 1576767879,
                            "updated_at": 1576767914,
                            "responsible_user_id": 123123,
                            "group_id": 0,
                            "entity_id": 1035487,
                            "entity_type": "leads",
                            "duration": 0,
                            "is_completed": true,
                            "task_type_id": 2,
                            "text": "Назначить встречу с клиентом",
                            "result": [],
                            "complete_till": 1576768179,
                            "account_id": 321312,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/tasks/215089"
                                }
                            }
                        }
                    ]
                }
            }
        """
        params = {k: v for k, v in locals().items() if k != 'self'}
        return self._get_entities('tasks', **params)

    def get_task(self, task_id: int) -> dict:
        """Get task
        Doc: https://www.amocrm.ru/developers/content/crm_platform/tasks-api#task-detail
        Args:
            task_id (int): id of task

        Returns:
            dict: {
                "id": 56981,
                "created_by": 54224,
                "updated_by": 3987910,
                "created_at": 1575910123,
                "updated_at": 1576767989,
                "responsible_user_id": 123123,
                "group_id": 0,
                "entity_id": 180765,
                "entity_type": "leads",
                "duration": 0,
                "is_completed": true,
                "task_type_id": 2,
                "text": "Назначить встречу с клиентом",
                "result": {
                    "text": "Результат есть"
                },
                "complete_till": 1575910423,
                "account_id": 321312,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/tasks/56981"
                    }
                }
            }
        """
        url = f'{self.crm_url}/api/v4/tasks/{task_id}'
        return self._send_api_request('get', url)

    def add_tasks(self, tasks: list) -> dict:
        """Add tasks
        Doc: https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-add
        Args:
            tasks (list): list of task objects

        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/tasks"
                    }
                },
                "_embedded": {
                    "tasks": [
                        {
                            "id": 4745251,
                            "updated_at": 1588760725,
                            "request_id": "0",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/tasks/4745251"
                                }
                            }
                        },
                        {
                            "id": 4747929,
                            "updated_at": 1588760725,
                            "request_id": "1",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/tasks/4747929"
                                }
                            }
                        }
                    ]
                }
            }
        """
        return self._create_or_update_entities('tasks', tasks)

    def update_tasks(self, tasks: list) -> dict:
        """Add tasks
        Doc: https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-edit
        Args:
            tasks (list): list of task objects

        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/tasks"
                    }
                },
                "_embedded": {
                    "tasks": [
                        {
                            "id": 4745251,
                            "updated_at": 1588760725,
                            "request_id": "0",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/tasks/4745251"
                                }
                            }
                        },
                        {
                            "id": 4747929,
                            "updated_at": 1588760725,
                            "request_id": "1",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/tasks/4747929"
                                }
                            }
                        }
                    ]
                }
            }
        """
        return self._create_or_update_entities('tasks', tasks, True)

    def execution_task(self, task_id: int, is_completed: bool, result: str) -> dict:
        """Executuin task
        Doc: https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-complete
        Args:
            task_id (int): id of task
            is_completed (bool): true if completed
            result: (str) text of result

        Returns:
            dict: {
                "is_completed": true,
                "result": {
                    "text": "Удалось связаться с клиентом"
                }
            }
        """
        url = f'{self.crm_url}/api/v4/tasks/{task_id}'
        params = {'is_completed': is_completed, 'result': {'text': result}}
        return self._send_api_request('patch', url, params)

    def get_tags_by_entity_type(
        self,
        entity_type: str,
        page: int = 1,
        limit: int = 250,
        filters: Optional[dict] = None,
    ) -> dict:
        """Get tags by entity_type
        Doc: https://www.amocrm.ru/developers/content/crm_platform/tags-api#tags-list
        Args:
            entity_type (str): leads|contacts|companies|customers
            page (int, optional): page number. Defaults to 1.
            limit (int, optional): limit of rows. Defaults to 250.
            filters (Optional[dict], optional): {'[name]': <name>}. Defaults to None.

        Returns:
            dict: {
                "_page": 1,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/tags?filter[id][]=2707&filter[id][]=2709&page=1&limit=50"
                    },
                    "next": {
                        "href": "https://example.amocrm.ru/api/v4/leads/tags?filter[id][]=2707&filter[id][]=2709&page=2&limit=50"
                    }
                },
                "_embedded": {
                    "tags": [
                        {
                            "id": 2707,
                            "name": "Заявка с сайта"
                        },
                        {
                            "id": 2709,
                            "name": "Техническая поддержка"
                        }
                    ]
                }
            }
        """
        params = {'page': page, 'limit': limit, 'filters': filters}
        return self._get_entities(f'{entity_type}/tags', **params)

    def add_tags_for_entity_type(self, entity_type: str, tags: list) -> dict:
        """Add tags for entity type
        Doc: https://www.amocrm.ru/developers/content/crm_platform/tags-api#tags-add
        Args:
            entity_type (str): leads|contacts|companies|customers
            tags (list): list of tags

        Returns:
            dict: {
                "_total_items": 3,
                "_embedded": {
                    "tags": [
                        {
                            "id": 263807,
                            "name": "Tag 1",
                            "request_id": "0"
                        },
                        {
                            "id": 263809,
                            "name": "Tag 2",
                            "request_id": "my_request_id"
                        },
                        {
                            "id": 263811,
                            "name": "Tag 3",
                            "request_id": "2"
                        }
                    ]
                }
            }
        """
        return self._create_or_update_entities(f'{entity_type}/tags/', tags)

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
        url = f'{self.crm_url}/api/v4/{entity_type}/custom_fields/{custom_field_id}'
        return self._send_api_request('get', url)

    def get_leads_custom_field(self, custom_field_id: int) -> dict:
        return self._get_custom_field_by_entity_type('leads', custom_field_id)

    def get_contacts_custom_field(self, custom_field_id: int) -> dict:
        return self._get_custom_field_by_entity_type('contacts', custom_field_id)

    def get_companies_custom_field(self, custom_field_id: int) -> dict:
        return self._get_custom_field_by_entity_type('companies', custom_field_id)

    def get_customers_custom_field(self, custom_field_id: int) -> dict:
        return self._get_custom_field_by_entity_type('customers', custom_field_id)

    def get_customers_segments_custom_field(self, custom_field_id: int) -> dict:
        return self._get_custom_field_by_entity_type(
            'customers/segments', custom_field_id
        )

    def get_customers_segments_custom_field(self, custom_field_id: int) -> dict:
        return self._get_custom_field_by_entity_type(
            'customers/segments', custom_field_id
        )

    def get_catalog_custom_field(self, catalog_id: int, custom_field_id: int) -> dict:
        return self._get_custom_field_by_entity_type(
            f'catalogs/{catalog_id}', custom_field_id
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
        url = f'{self.crm_url}/{entity_type}/custom_fields/'
        return self._send_api_request('post', url,)

    def create_leads_custom_fields(self, custom_fields: list) -> dict:
        return self._create_custom_fields('leads', custom_fields)

    def create_contacts_custom_fields(self, custom_fields: list) -> dict:
        return self._create_custom_fields('contacts', custom_fields)

    def create_companies_custom_fields(self, custom_fields: list) -> dict:
        return self._create_custom_fields('companies', custom_fields)

    def create_customers_custom_fields(self, custom_fields: list) -> dict:
        return self._create_custom_fields('customers', custom_fields)

    def create_customers_segments_custom_fields(self, custom_fields: list) -> dict:
        return self._create_custom_fields('customers/segments', custom_fields)

    def create_catalog_custom_fields(
        self, catalog_id: int, custom_fields: list
    ) -> dict:
        return self._create_custom_fields(f'catalogs/{catalog_id}', custom_fields)

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
        url = f'{self.crm_url}/{entity_type}/custom_fields/'
        return self._send_api_request('patch', url, custom_fields)

    def update_leads_custom_fields(self, custom_fields: list) -> dict:
        return self._update_custom_fields('leads', custom_fields)

    def update_contacts_custom_fields(self, custom_fields: list) -> dict:
        return self._update_custom_fields('contacts', custom_fields)

    def update_companies_custom_fields(self, custom_fields: list) -> dict:
        return self._update_custom_fields('companies', custom_fields)

    def update_customers_custom_fields(self, custom_fields: list) -> dict:
        return self._update_custom_fields('customers', custom_fields)

    def updatecustomers_segments_custom_fields(self, custom_fields: list) -> dict:
        return self._update_custom_fields('customers/segments', custom_fields)

    def update_catalog_custom_fields(
        self, catalog_id: int, custom_fields: list
    ) -> dict:
        return self._update_custom_fields(f'catalogs/{catalog_id}', custom_fields)
