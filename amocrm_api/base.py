from .entities import (
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
)
from .entities.base import mask_token as mask_token


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
