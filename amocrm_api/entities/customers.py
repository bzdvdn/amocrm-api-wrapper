from .base import Entity

from typing import Optional

class Customers(Entity):
    def unlink_customers_entity(self, entity_id: int, objects: list) -> dict:
        return self._unlink_entities("customers", entity_id, objects)

    def link_customers_entity(self, entity_id: int, objects: list) -> dict:
        return self._link_entities("customers", entity_id, objects)

    def get_customers_links(
        self, entity_id: int, filters: Optional[dict] = None
    ) -> dict:
        return self._get_entity_links("customers", entity_id, filters)

    async def unlink_customers_entity_async(
        self, entity_id: int, objects: list
    ) -> dict:
        """Async version of unlink_customers_entity."""
        return await self._unlink_entities_async("customers", entity_id, objects)

    async def link_customers_entity_async(
        self, entity_id: int, objects: list
    ) -> dict:
        """Async version of link_customers_entity."""
        return await self._link_entities_async("customers", entity_id, objects)

    async def get_customers_links_async(
        self, entity_id: int, filters: Optional[dict] = None
    ) -> dict:
        """Async version of get_customers_links."""
        return await self._get_entity_links_async("customers", entity_id, filters)
