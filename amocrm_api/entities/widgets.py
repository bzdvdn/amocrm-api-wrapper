from typing import Any
from urllib.parse import urlencode

from .base import Entity


class Widgets(Entity):
    def _build_get_widgets_url(self, page: int, limit: int) -> str:
        url = f"{self.crm_url}/api/v4/widgets"
        params = {"page": page, "limit": limit}
        return f"{url}?{urlencode(params)}"

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
        url = self._build_get_widgets_url(page, limit)
        return self._send_api_request("get", url)

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
        url = f"{self.crm_url}/api/v4/widgets/{widget_code}"
        return self._send_api_request("get", url)

    def install_widget(self, widget_code: str, **kwargs: Any) -> dict:
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
        url = f"{self.crm_url}/api/v4/widgets/{widget_code}"
        return self._send_api_request("post", url, kwargs)

    def uninstall_widget(self, widget_code: str) -> dict:
        """Uninstall widget
        Doc: https://www.amocrm.ru/developers/content/crm_platform/widgets-api#widget-uninstall
        Args:
            widget_code (str): code of widget
    
        Returns:
            dict: {}
        """
    
        url = f"{self.crm_url}/api/v4/widgets/{widget_code}"
        return self._send_api_request("delete", url)

    async def get_widgets_async(self, page: int = 1, limit: int = 250) -> dict:
        """Async version of get_widgets."""
        url = self._build_get_widgets_url(page, limit)
        return await self._send_api_request_async("get", url)

    async def get_widget_async(self, widget_code: str) -> dict:
        """Async version of get_widget."""
        url = f"{self.crm_url}/api/v4/widgets/{widget_code}"
        return await self._send_api_request_async("get", url)

    async def install_widget_async(self, widget_code: str, **kwargs: Any) -> dict:
        """Async version of install_widget."""
        url = f"{self.crm_url}/api/v4/widgets/{widget_code}"
        return await self._send_api_request_async("post", url, kwargs)

    async def uninstall_widget_async(self, widget_code: str) -> dict:
        """Async version of uninstall_widget."""
        url = f"{self.crm_url}/api/v4/widgets/{widget_code}"
        return await self._send_api_request_async("delete", url)
