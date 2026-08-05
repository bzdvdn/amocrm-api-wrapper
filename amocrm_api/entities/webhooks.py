from urllib.parse import urlencode

from .base import Entity


class Webhooks(Entity):
    def _build_get_webhooks_url(self, distansion: str | None) -> str:
        url = f"{self.crm_url}/api/v4/webhooks"
        if distansion:
            params = {"filter[distansion]": distansion}
            url = f"{url}?{urlencode(params)}"
        return url

    def _build_subscribe_webhook_params(
        self,
        destination: str,
        settings: list,
    ) -> dict:
        return {"destination": destination, "settings": settings}

    def get_webhooks(self, distansion: str | None = None) -> dict:
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
        url = self._build_get_webhooks_url(distansion)
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
        params = self._build_subscribe_webhook_params(destination, settings)
        return self._send_api_request("post", url, data=params)

    def unsubscribe_webhook(self) -> dict:
        """
        Doc: https://www.amocrm.ru/developers/content/crm_platform/webhooks-api#webhooks-delete
        """
        url = f"{self.crm_url}/api/v4/webhooks"
        return self._send_api_request("delete", url)

    async def get_webhooks_async(self, distansion: str | None = None) -> dict:
        """Async version of get_webhooks."""
        url = self._build_get_webhooks_url(distansion)
        return await self._send_api_request_async("get", url)

    async def subscribe_webhook_async(
        self, destination: str, settings: list
    ) -> dict:
        """Async version of subscribe_webhook."""
        url = f"{self.crm_url}/api/v4/webhooks"
        params = self._build_subscribe_webhook_params(destination, settings)
        return await self._send_api_request_async("post", url, data=params)

    async def unsubscribe_webhook_async(self) -> dict:
        """Async version of unsubscribe_webhook."""
        url = f"{self.crm_url}/api/v4/webhooks"
        return await self._send_api_request_async("delete", url)
