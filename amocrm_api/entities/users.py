from urllib.parse import urlencode

from .base import Entity


class Users(Entity):
    def _build_get_users_url(
        self,
        page: int,
        limit: int,
        with_role: bool,
        with_group: bool,
    ) -> str:
        url = f"{self.crm_url}/api/v4/users"
        params = {"page": page, "limit": limit}
        with_ = []
        if with_group:
            with_.append("group")
        if with_role:
            with_.append("role")
        url = f"{url}?{urlencode(params)}"
        if with_:
            with_str = ",".join(i for i in with_)
            url = f"{url}&with={with_str}"
        return url

    def _build_get_user_url(
        self,
        user_id: int,
        with_role: bool,
        with_group: bool,
    ) -> str:
        url = f"{self.crm_url}/api/v4/users/{user_id}"
        with_ = []
        if with_group:
            with_.append("group")
        if with_role:
            with_.append("role")
        if with_:
            with_str = ",".join(i for i in with_)
            url = f"{url}?with={with_str}"
        return url

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
        url = self._build_get_users_url(page, limit, with_role, with_group)
        return self._send_api_request("get", url)

    def get_user(
        self,
        user_id: int,
        with_role: bool = False,
        with_group: bool = False,
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
        url = self._build_get_user_url(user_id, with_role, with_group)
        return self._send_api_request("get", url)

    async def get_users_async(
        self,
        page: int = 1,
        limit: int = 250,
        with_role: bool = False,
        with_group: bool = False,
    ) -> dict:
        """Async version of get_users."""
        url = self._build_get_users_url(page, limit, with_role, with_group)
        return await self._send_api_request_async("get", url)

    async def get_user_async(
        self,
        user_id: int,
        with_role: bool = False,
        with_group: bool = False,
    ) -> dict:
        """Async version of get_user."""
        url = self._build_get_user_url(user_id, with_role, with_group)
        return await self._send_api_request_async("get", url)
