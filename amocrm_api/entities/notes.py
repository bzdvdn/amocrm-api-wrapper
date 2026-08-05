from urllib.parse import urlencode

from .base import Entity


class Notes(Entity):
    def _build_get_notes_by_entity_type_url(
        self,
        entity_type: str,
        page: int,
        limit: int,
        filter_by_id: int | list | None,
        filter_by_entity_id: list | None,
        filter_by_note_type: list | str | None,
        filter_by_updated_at: int | None,
        filter_by_updated_at_from: int | None,
        filter_by_updated_at_to: int | None,
        order_by_updated_at: str,
        order_by_id: str,
    ) -> str:
        url = f"{self.crm_url}/api/v4/{entity_type}/notes"
        params: dict = {"page": page, "limit": limit}
        if filter_by_id:
            params["filter[id][]" if isinstance(filter_by_id, list) else "filter[id]"] = filter_by_id
        if filter_by_note_type:
            params["filter[note_type][]" if isinstance(filter_by_note_type, list) else "filter[note_type]"] = filter_by_note_type
        if filter_by_entity_id:
            params["filter[entity_id][]"] = filter_by_entity_id
        if filter_by_updated_at:
            params["filter[updated_at]"] = filter_by_updated_at
        if filter_by_updated_at_from:
            params["filter[updated_at][from]"] = filter_by_updated_at_from
        if filter_by_updated_at_to:
            params["filter[updated_at][to]"] = filter_by_updated_at_to
        if order_by_updated_at:
            params["order[updated_at]"] = order_by_updated_at
        if order_by_id:
            params["order[id]"] = order_by_id

        return f"{url}?{urlencode(params, doseq=True)}"

    def _build_get_notes_by_entity_type_and_entity_id_url(
        self,
        entity_type: str,
        entity_id: int,
        page: int,
        limit: int,
        filter_by_id: int | list | None,
        filter_by_note_type: list | str | None,
        filter_by_updated_at: int | None,
        filter_by_updated_at_from: int | None,
        filter_by_updated_at_to: int | None,
        order_by_updated_at: str,
        order_by_id: str,
    ) -> str:
        url = f"{self.crm_url}/api/v4/{entity_type}/{entity_id}/notes"
        params: dict = {"page": page, "limit": limit}
        if filter_by_id:
            params["filter[id][]" if isinstance(filter_by_id, list) else "filter[id]"] = filter_by_id
        if filter_by_note_type:
            params["filter[note_type][]" if isinstance(filter_by_note_type, list) else "filter[note_type]"] = filter_by_note_type
        if filter_by_updated_at:
            params["filter[updated_at]"] = filter_by_updated_at
        if filter_by_updated_at_from:
            params["filter[updated_at][from]"] = filter_by_updated_at_from
        if filter_by_updated_at_to:
            params["filter[updated_at][to]"] = filter_by_updated_at_to
        if order_by_updated_at:
            params["order[updated_at]"] = order_by_updated_at
        if order_by_id:
            params["order[id]"] = order_by_id

        return f"{url}?{urlencode(params, doseq=True)}"

    def _build_get_entity_note_url(
        self,
        entity_type: str,
        id_: int,
        entity_id: int | None,
    ) -> str:
        if entity_id:
            return f"{self.crm_url}/api/v4/{entity_type}/{entity_id}/notes/{id_}"
        return f"{self.crm_url}/api/v4/{entity_type}/notes/{id_}"

    def _build_notes_url(
        self,
        entity_type: str,
        entity_id: int | None,
    ) -> str:
        if entity_id:
            return f"{self.crm_url}/api/v4/{entity_type}/{entity_id}/notes"
        return f"{self.crm_url}/api/v4/{entity_type}/notes"

    def get_notes_by_entity_type(
        self,
        entity_type: str,
        page: int = 1,
        limit: int = 250,
        filter_by_id: int | list | None = None,
        filter_by_entity_id: list | None = None,
        filter_by_note_type: list | str | None = None,
        filter_by_updated_at: int | None = None,
        filter_by_updated_at_from: int | None = None,
        filter_by_updated_at_to: int | None = None,
        order_by_updated_at: str = "asc",
        order_by_id: str = "asc",
    ) -> dict:
        """Get notes by event type
    
        Args:
            entity_type (str): entity type
            page (int, optional): page. Defaults to 1.
            limit (int, optional): limit per page. Defaults to 250.
            filter_by_id (Union[int, list, None], optional): list or id. Defaults to None.
            filter_by_entity_id (Optional[list], optional): list or entity id. Defaults to None.
            filter_by_note_type (Optional[Union[list, str]], optional): list of not types. Defaults to None.
            filter_by_updated_at (Optional[int], optional): timestamp. Defaults to None.
            filter_by_updated_at_from (Optional[int], optional): timestamp. Defaults to None.
            filter_by_updated_at_to (Optional[int], optional): timestamp. Defaults to None.
            order_by_updated_at (str): asc or decs. Defaults to asc.
            order_by_id (str): asc or decs. Defaults to asc.
    
        Returns:
            dict: {
                "_page": 1,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/notes?filter[id][0]=42709325&filter[id][1]=42709842&page=1&limit=50"
                    },
                    "next": {
                        "href": "https://example.amocrm.ru/api/v4/leads/notes?filter[id][0]=42709325&filter[id][1]=42709842&page=2&limit=50"
                    }
                },
                "_embedded": {
                    "notes": [
                        {
                            "id": 42709325,
                            "entity_id": 26050861,
                            "created_by": 940088,
                            "updated_by": 940088,
                            "created_at": 1540407495,
                            "updated_at": 1540408317,
                            "responsible_user_id": 939801,
                            "group_id": 0,
                            "note_type": "common",
                            "params": {
                                "text": "Текст примечания"
                            },
                            "account_id": 17079858,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/26050861/notes/42709325"
                                }
                            }
                        },
                        {
                            "id": 42709842,
                            "entity_id": 26053794,
                            "created_by": 939801,
                            "updated_by": 939801,
                            "created_at": 1548280113,
                            "updated_at": 1548280115,
                            "responsible_user_id": 939801,
                            "group_id": 0,
                            "note_type": "attachment",
                            "params": {
                                "original_name": "Снимок экрана 2020-05-16 в 13.12.20.png",
                                "attachment": "gijy_Snimok_ekrana_2020-05-16_v_13.12.20.png"
                            },
                            "account_id": 17079858,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/26053794/notes/42709842"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = self._build_get_notes_by_entity_type_url(
            entity_type,
            page,
            limit,
            filter_by_id,
            filter_by_entity_id,
            filter_by_note_type,
            filter_by_updated_at,
            filter_by_updated_at_from,
            filter_by_updated_at_to,
            order_by_updated_at,
            order_by_id,
        )
        return self._send_api_request("get", url)

    def get_notes_by_entity_type_and_entity_id(
        self,
        entity_type: str,
        entity_id: int,
        page: int = 1,
        limit: int = 250,
        filter_by_id: int | list | None = None,
        filter_by_note_type: list | str | None = None,
        filter_by_updated_at: int | None = None,
        filter_by_updated_at_from: int | None = None,
        filter_by_updated_at_to: int | None = None,
        order_by_updated_at: str = "asc",
        order_by_id: str = "asc",
    ) -> dict:
        """Get notes by event type and entity id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#notes-entity-list
        Args:
            entity_type (str): entity type
            event_type (int): entity id
            page (int, optional): page. Defaults to 1.
            limit (int, optional): limit per page. Defaults to 250.
            filter_by_id (Union[int, list, None], optional): list or id. Defaults to None.
            filter_by_entity_id (Optional[list], optional): list or entity id. Defaults to None.
            filter_by_note_type (Optional[Union[list, str]], optional): list of not types. Defaults to None.
            filter_by_updated_at (Optional[int], optional): timestamp. Defaults to None.
            filter_by_updated_at_from (Optional[int], optional): timestamp. Defaults to None.
            filter_by_updated_at_to (Optional[int], optional): timestamp. Defaults to None.
            order_by_updated_at (str): asc or decs. Defaults to asc.
            order_by_id (str): asc or decs. Defaults to asc.
    
        Returns:
            dict: {
                "_page": 1,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/26050861/notes?limit=2&page=1"
                    },
                    "next": {
                        "href": "https://example.amocrm.ru/api/v4/leads/26050861/notes?limit=2&page=2"
                    }
                },
                "_embedded": {
                    "notes": [
                        {
                            "id": 42709325,
                            "entity_id": 26050861,
                            "created_by": 940088,
                            "updated_by": 940088,
                            "created_at": 1540407495,
                            "updated_at": 1540408317,
                            "responsible_user_id": 939801,
                            "group_id": 0,
                            "note_type": "common",
                            "params": {
                                "text": "Текст примечания 2"
                            },
                            "account_id": 17079858,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/26050861/notes/42709325"
                                }
                            }
                        },
                        {
                            "id": 42736075,
                            "entity_id": 26050861,
                            "created_by": 939801,
                            "updated_by": 939801,
                            "created_at": 1587555198,
                            "updated_at": 1587555199,
                            "responsible_user_id": 939801,
                            "group_id": 0,
                            "note_type": "common",
                            "params": {
                                "text": "Текст примечания"
                            },
                            "account_id": 17079858,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/26050861/notes/42736075"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = self._build_get_notes_by_entity_type_and_entity_id_url(
            entity_type,
            entity_id,
            page,
            limit,
            filter_by_id,
            filter_by_note_type,
            filter_by_updated_at,
            filter_by_updated_at_from,
            filter_by_updated_at_to,
            order_by_updated_at,
            order_by_id,
        )
        return self._send_api_request("get", url)

    def get_entity_note(
        self, entity_type: str, id_: int, entity_id: int | None = None
    ) -> dict:
        """get entity note
        Doc: https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#note-detail
        Args:
            entity_type (str): entity type
            id_ (int): note id
            entity_id (Optional[int], optional): entity id. Defaults to None.
    
        Returns:
            dict: {
                "id": 42709325,
                "entity_id": 26050861,
                "created_by": 940088,
                "updated_by": 940088,
                "created_at": 1540407495,
                "updated_at": 1540408317,
                "responsible_user_id": 939801,
                "group_id": 0,
                "note_type": "common",
                "params": {
                    "text": "Текст примечания"
                },
                "account_id": 17079858,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/26050861/notes/42709325"
                    }
                }
            }
        """
        url = self._build_get_entity_note_url(entity_type, id_, entity_id)
        return self._send_api_request("get", url)

    def create_entity_note(
        self, entity_type: str, notes: list, entity_id: int | None = None
    ) -> dict:
        """create entity note
        Doc: https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#notes-add
        Args:
            entity_type (str): entity type
            notes (list): list of notes
            entity_id (Optional[int], optional): entity id. Defaults to None.
    
        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "http://example.amocrm.ru/api/v4/leads/notes"
                    }
                },
                "_embedded": {
                    "notes": [
                        {
                            "id": 76787983,
                            "entity_id": 167353,
                            "request_id": "0",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/167353/notes/76787983"
                                }
                            }
                        },
                        {
                            "id": 76787985,
                            "entity_id": 167353,
                            "request_id": "1",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/167353/notes/76787985"
                                }
                            }
                        },
                        {
                            "id": 76787987,
                            "entity_id": 167353,
                            "request_id": "2",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/167353/notes/76787987"
                                }
                            }
                        },
                        {
                            "id": 76787989,
                            "entity_id": 167353,
                            "request_id": "3",
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/167353/notes/76787989"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = self._build_notes_url(entity_type, entity_id)
        return self._send_api_request("post", url, data=notes)

    def update_entity_note(
        self, entity_type: str, entity_id: int, id_: int, params: dict
    ) -> dict:
        """update single entity note
        Doc: https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#notes-edit
        Args:
            entity_type (str): entity type
            entity_id (int): entity_id
            id_ (int): note id
            params (dict): full note model like {'note_type': 'common', 'params': {'text': 'hi'}}

        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/notes"
                    }
                },
                "_embedded": {
                    "notes": [
                        {
                            "id": 76610421,
                            "entity_id": 167353,
                            "updated_at": 1588841241,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/167353/notes/76610421"
                                }
                            }
                        },
                        {
                            "id": 76610423,
                            "entity_id": 167353,
                            "updated_at": 1588841241,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/167353/notes/76610423"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = f"{self.crm_url}/api/v4/{entity_type}/{entity_id}/notes/{id_}"
        params = dict(params)
        params["id"] = id_
        return self._send_api_request("patch", url, params)

    def update_entity_many_notes(
        self,
        entity_type: str,
        notes: list,
        entity_id: int | None = None,
    ) -> dict:
        """update many entity note
        Doc: https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#notes-edit
        Args:
            entity_type (str): entity type
            notes (list): list of notes
            entity_id (Optional[int], optional): entity id. Defaults to None.
    
        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/notes"
                    }
                },
                "_embedded": {
                    "notes": [
                        {
                            "id": 76610421,
                            "entity_id": 167353,
                            "updated_at": 1588841241,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/167353/notes/76610421"
                                }
                            }
                        },
                        {
                            "id": 76610423,
                            "entity_id": 167353,
                            "updated_at": 1588841241,
                            "_links": {
                                "self": {
                                    "href": "https://example.amocrm.ru/api/v4/leads/167353/notes/76610423"
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = self._build_notes_url(entity_type, entity_id)
        return self._send_api_request("patch", url, data=notes)

    async def get_notes_by_entity_type_async(
        self,
        entity_type: str,
        page: int = 1,
        limit: int = 250,
        filter_by_id: int | list | None = None,
        filter_by_entity_id: list | None = None,
        filter_by_note_type: list | str | None = None,
        filter_by_updated_at: int | None = None,
        filter_by_updated_at_from: int | None = None,
        filter_by_updated_at_to: int | None = None,
        order_by_updated_at: str = "asc",
        order_by_id: str = "asc",
    ) -> dict:
        """Async version of get_notes_by_entity_type."""
        url = self._build_get_notes_by_entity_type_url(
            entity_type,
            page,
            limit,
            filter_by_id,
            filter_by_entity_id,
            filter_by_note_type,
            filter_by_updated_at,
            filter_by_updated_at_from,
            filter_by_updated_at_to,
            order_by_updated_at,
            order_by_id,
        )
        return await self._send_api_request_async("get", url)

    async def get_notes_by_entity_type_and_entity_id_async(
        self,
        entity_type: str,
        entity_id: int,
        page: int = 1,
        limit: int = 250,
        filter_by_id: int | list | None = None,
        filter_by_note_type: list | str | None = None,
        filter_by_updated_at: int | None = None,
        filter_by_updated_at_from: int | None = None,
        filter_by_updated_at_to: int | None = None,
        order_by_updated_at: str = "asc",
        order_by_id: str = "asc",
    ) -> dict:
        """Async version of get_notes_by_entity_type_and_entity_id."""
        url = self._build_get_notes_by_entity_type_and_entity_id_url(
            entity_type,
            entity_id,
            page,
            limit,
            filter_by_id,
            filter_by_note_type,
            filter_by_updated_at,
            filter_by_updated_at_from,
            filter_by_updated_at_to,
            order_by_updated_at,
            order_by_id,
        )
        return await self._send_api_request_async("get", url)

    async def get_entity_note_async(
        self, entity_type: str, id_: int, entity_id: int | None = None
    ) -> dict:
        """Async version of get_entity_note."""
        url = self._build_get_entity_note_url(entity_type, id_, entity_id)
        return await self._send_api_request_async("get", url)

    async def create_entity_note_async(
        self, entity_type: str, notes: list, entity_id: int | None = None
    ) -> dict:
        """Async version of create_entity_note."""
        url = self._build_notes_url(entity_type, entity_id)
        return await self._send_api_request_async("post", url, data=notes)

    async def update_entity_note_async(
        self, entity_type: str, entity_id: int, id_: int, params: dict
    ) -> dict:
        """Async version of update_entity_note."""
        url = f"{self.crm_url}/api/v4/{entity_type}/{entity_id}/notes/{id_}"
        params = dict(params)
        params["id"] = id_
        return await self._send_api_request_async("patch", url, params)

    async def update_entity_many_notes_async(
        self,
        entity_type: str,
        notes: list,
        entity_id: int | None = None,
    ) -> dict:
        """Async version of update_entity_many_notes."""
        url = self._build_notes_url(entity_type, entity_id)
        return await self._send_api_request_async("patch", url, data=notes)
