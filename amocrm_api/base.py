from .entities import (
    Catalogs,
    Companies,
    Contacts,
    Customers,
    CustomFields,
    Events,
    Leads,
    Notes,
    Pipelines,
    Tags,
    Tasks,
    Unsorted,
    Users,
    Webhooks,
    Widgets,
)
from .entities.base import mask_token as mask_token  # noqa: PLC0414 (re-export)


class BaseClient(
    Leads,
    Unsorted,
    Pipelines,
    Contacts,
    Companies,
    Customers,
    Catalogs,
    CustomFields,
    Users,
    Webhooks,
    Widgets,
    Tasks,
    Tags,
    Events,
    Notes,
):
    """Aggregates all amocrm entities into a single client interface."""
