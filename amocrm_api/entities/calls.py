from .base import Entity


class Calls(Entity):
    def create_calls(self, calls: list) -> dict:
        """Add calls to entity cards
        Doc: https://www.amocrm.ru/developers/content/crm_platform/calls-api#calls-add
        Args:
            calls (list): list of calls

        Returns:
            dict: {
                "_total_items": 1,
                "errors": [],
                "_embedded": {
                    "calls": [
                        {
                            "id": 37512063,
                            "entity_id": 11070881,
                            "entity_type": "contact",
                            "account_id": 28805383,
                            "request_id": "0",
                            "_embedded": {
                                "entity": {
                                    "id": 11070881,
                                    "_links": {
                                        "self": {
                                            "href": "https://example.amocrm.ru/api/v4/contacts/11070881"
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        """
        url = f"{self.crm_url}/api/v4/calls"
        return self._send_api_request("post", url, calls)

    async def create_calls_async(self, calls: list) -> dict:
        """Async version of create_calls."""
        url = f"{self.crm_url}/api/v4/calls"
        return await self._send_api_request_async("post", url, calls)
