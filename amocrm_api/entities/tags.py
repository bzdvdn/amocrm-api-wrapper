
from collections.abc import AsyncIterator, Iterator

from .base import Entity


class Tags(Entity):
    def get_tags_by_entity_type(
        self,
        entity_type: str,
        page: int = 1,
        limit: int = 250,
        filters: dict | None = None,
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
        params: dict = {"page": page, "limit": limit, "filters": filters}
        return self._get_entities(f"{entity_type}/tags", **params)

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
        return self._create_or_update_entities(f"{entity_type}/tags", tags)

    async def get_tags_by_entity_type_async(
        self,
        entity_type: str,
        page: int = 1,
        limit: int = 250,
        filters: dict | None = None,
    ) -> dict:
        """Async version of get_tags_by_entity_type."""
        params: dict = {"page": page, "limit": limit, "filters": filters}
        return await self._get_entities_async(f"{entity_type}/tags", **params)

    def iter_tags_by_entity_type(
        self,
        entity_type: str,
        limit: int = 250,
        filters: dict | None = None,
    ) -> Iterator[dict]:
        """Iterate over all tags of an entity type across pages."""
        return self._iter_entities(
            f"{entity_type}/tags", limit, None, filters, None, None, "tags"
        )

    async def iter_tags_by_entity_type_async(
        self,
        entity_type: str,
        limit: int = 250,
        filters: dict | None = None,
    ) -> AsyncIterator[dict]:
        """Async version of iter_tags_by_entity_type."""
        async for tag in self._iter_entities_async(
            f"{entity_type}/tags", limit, None, filters, None, None, "tags"
        ):
            yield tag

    async def add_tags_for_entity_type_async(
        self, entity_type: str, tags: list
    ) -> dict:
        """Async version of add_tags_for_entity_type."""
        return await self._create_or_update_entities_async(
            f"{entity_type}/tags", tags
        )
