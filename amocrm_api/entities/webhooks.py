from .base import Entity

from typing import Optional
from urllib.parse import urlencode

class Webhooks(Entity):
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
        url = f"{self.crm_url}/api/v4/webhooks"
        if distansion:
            params = {"filter[distansion]": distansion}
            url = f"{url}?{urlencode(params)}"
        return self._send_api_request("get", url)

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
        url = f"{self.crm_url}/api/v4/webhooks"
        params = {"destination": destination, "settings": settings}
        return self._send_api_request("post", url, data=params)

    def unsubscribe_webhook(self):
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/webhooks-api#webhooks-delete
        """
        url = f"{self.crm_url}/api/v4/webhooks"
        return self._send_api_request("delete", url)
