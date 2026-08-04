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
