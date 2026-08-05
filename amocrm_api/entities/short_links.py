from .base import Entity


class ShortLinks(Entity):
    def create_short_links(self, short_links: list) -> dict:
        """Create short links
        Doc: https://www.amocrm.ru/developers/content/crm_platform/short_links
        Args:
            short_links (list): list of short links

        Returns:
            dict: {
                "_links": {
                    "self": {
                        "href": "/api/v4/short_links"
                    }
                },
                "_embedded": {
                    "short_links": [
                        {
                            "url": "https://amo.sh/XXXXXXXXXXXX",
                            "account_id": 123,
                            "metadata": {
                                "entity_type": "contacts",
                                "entity_id": 321
                            }
                        }
                    ]
                }
            }
        """
        url = f"{self.crm_url}/api/v4/short_links"
        return self._send_api_request("post", url, short_links)

    async def create_short_links_async(self, short_links: list) -> dict:
        """Async version of create_short_links."""
        url = f"{self.crm_url}/api/v4/short_links"
        return await self._send_api_request_async("post", url, short_links)
