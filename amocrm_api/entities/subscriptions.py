from urllib.parse import urlencode

from .base import Entity


class Subscriptions(Entity):
    def _build_get_subscriptions_url(
        self,
        entity_type: str,
        entity_id: int,
        page: int,
        limit: int,
    ) -> str:
        url = f"{self.crm_url}/api/v4/{entity_type}/{entity_id}/subscriptions"
        params: dict = {"page": page, "limit": limit}
        return f"{url}?{urlencode(params)}"

    def get_subscriptions(
        self,
        entity_type: str,
        entity_id: int,
        page: int = 1,
        limit: int = 250,
    ) -> dict:
        """Get entity subscriptions
        Doc: https://www.amocrm.ru/developers/content/crm_platform/subscriptions-api#subscriptions-list
        Args:
            entity_type (str): entity type (leads, customers)
            entity_id (int): entity id
            page (int, optional): page number. Defaults to 1.
            limit (int, optional): limit per page. Defaults to 250.

        Returns:
            dict: {
                "_total_items": 2,
                "_page": 1,
                "_page_count": 1,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/667999637/subscriptions?page=1&limit=50"
                    }
                },
                "_embedded": {
                    "subscriptions": [
                        {
                            "subscriber_id": 964291,
                            "type": "user"
                        },
                        {
                            "subscriber_id": 1150,
                            "type": "group"
                        }
                    ]
                }
            }
        """
        url = self._build_get_subscriptions_url(
            entity_type, entity_id, page, limit
        )
        return self._send_api_request("get", url)

    async def get_subscriptions_async(
        self,
        entity_type: str,
        entity_id: int,
        page: int = 1,
        limit: int = 250,
    ) -> dict:
        """Async version of get_subscriptions."""
        url = self._build_get_subscriptions_url(
            entity_type, entity_id, page, limit
        )
        return await self._send_api_request_async("get", url)
