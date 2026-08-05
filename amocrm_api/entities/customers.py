
from collections.abc import AsyncIterator, Iterator
from urllib.parse import urlencode

from .base import Entity


class Customers(Entity):
    def unlink_customers_entity(self, entity_id: int, objects: list) -> dict:
        return self._unlink_entities("customers", entity_id, objects)

    def link_customers_entity(self, entity_id: int, objects: list) -> dict:
        return self._link_entities("customers", entity_id, objects)

    def get_customers_links(
        self, entity_id: int, filters: dict | None = None
    ) -> dict:
        return self._get_entity_links("customers", entity_id, filters)

    def set_customers_mode(self, mode: str, is_enabled: bool) -> dict:
        """Enable/disable customers and switch their mode
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-api#customers-mode
        Args:
            mode (str): segments or periodicity
            is_enabled (bool): enable/disable customers functionality
        """
        url = f"{self.crm_url}/api/v4/customers/mode"
        params = {"mode": mode, "is_enabled": is_enabled}
        return self._send_api_request("patch", url, params)

    def get_customers(
        self,
        limit: int = 250,
        page: int = 1,
        with_params: list | None = None,
        filters: dict | None = None,
        order: dict | None = None,
        query: str | None = None,
    ) -> dict:
        """Get customers
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-api#customers-list
        """
        params: dict = {k: v for k, v in locals().items() if k != "self"}
        return self._get_entities("customers", **params)

    def get_customer(self, customer_id: int, with_params: list | None = None) -> dict:
        """Get customer by id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-api#customer-detail
        """
        url = f"{self.crm_url}/api/v4/customers/{customer_id}"
        if with_params:
            url += "?with=" + ",".join(param for param in with_params)
        return self._send_api_request("get", url)

    def create_customers(self, customers: list) -> dict:
        """Create customers
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-api#customers-add
        """
        return self._create_or_update_entities("customers", customers)

    def update_customers(self, customers: list) -> dict:
        """Update customers
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-api#customers-edit
        """
        return self._create_or_update_entities("customers", customers, True)

    def get_transactions(
        self,
        customer_id: int | None = None,
        limit: int = 250,
        page: int = 1,
        filter_by_ids: int | list | None = None,
    ) -> dict:
        """Get transactions
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-api#customers-transactions-list
        """
        url = (
            f"{self.crm_url}/api/v4/customers/{customer_id}/transactions"
            if customer_id is not None
            else f"{self.crm_url}/api/v4/customers/transactions"
        )
        params: dict = {"limit": limit, "page": page}
        if filter_by_ids:
            params["filter[id][]" if isinstance(filter_by_ids, list) else "filter[id]"] = (
                filter_by_ids
            )
        return self._send_api_request("get", f"{url}?{urlencode(params, doseq=True)}")

    def get_transaction(
        self, transaction_id: int, customer_id: int | None = None
    ) -> dict:
        """Get transaction by id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-api#customers-transactions-detail
        """
        url = (
            f"{self.crm_url}/api/v4/customers/{customer_id}/transactions/{transaction_id}"
            if customer_id is not None
            else f"{self.crm_url}/api/v4/customers/transactions/{transaction_id}"
        )
        return self._send_api_request("get", url)

    def create_transactions(self, customer_id: int, transactions: list) -> dict:
        """Add transactions to customer
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-api#customers-transactions-add
        """
        url = f"{self.crm_url}/api/v4/customers/{customer_id}/transactions"
        return self._send_api_request("post", url, transactions)

    def delete_transaction(
        self, transaction_id: int, customer_id: int | None = None
    ) -> dict:
        """Delete transaction by id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-api#customers-transactions-delete
        """
        url = (
            f"{self.crm_url}/api/v4/customers/{customer_id}/transactions/{transaction_id}"
            if customer_id is not None
            else f"{self.crm_url}/api/v4/customers/transactions/{transaction_id}"
        )
        return self._send_api_request("delete", url)

    def change_bonus_points(self, customer_id: int, points: dict) -> dict:
        """Accrue or redeem bonus points for customer
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-api#customers-bonus-points
        Args:
            customer_id (int): customer id
            points (dict): {'earn': int} or {'redeem': int}
        """
        url = f"{self.crm_url}/api/v4/customers/{customer_id}/bonus_points"
        return self._send_api_request("post", url, points)

    def iter_customers(
        self,
        limit: int = 250,
        with_params: list | None = None,
        filters: dict | None = None,
        order: dict | None = None,
        query: str | None = None,
    ) -> Iterator[dict]:
        """Iterate over all customers across pages."""
        return self._iter_entities(
            "customers", limit, with_params, filters, None, order, "customers", query
        )

    async def iter_customers_async(
        self,
        limit: int = 250,
        with_params: list | None = None,
        filters: dict | None = None,
        order: dict | None = None,
        query: str | None = None,
    ) -> AsyncIterator[dict]:
        """Async version of iter_customers."""
        async for customer in self._iter_entities_async(
            "customers", limit, with_params, filters, None, order, "customers", query
        ):
            yield customer

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
        self, entity_id: int, filters: dict | None = None
    ) -> dict:
        """Async version of get_customers_links."""
        return await self._get_entity_links_async("customers", entity_id, filters)

    async def set_customers_mode_async(self, mode: str, is_enabled: bool) -> dict:
        """Async version of set_customers_mode."""
        url = f"{self.crm_url}/api/v4/customers/mode"
        params = {"mode": mode, "is_enabled": is_enabled}
        return await self._send_api_request_async("patch", url, params)

    async def get_customers_async(
        self,
        limit: int = 250,
        page: int = 1,
        with_params: list | None = None,
        filters: dict | None = None,
        order: dict | None = None,
        query: str | None = None,
    ) -> dict:
        """Async version of get_customers."""
        params = {k: v for k, v in locals().items() if k != "self"}
        return await self._get_entities_async("customers", **params)

    async def get_customer_async(
        self, customer_id: int, with_params: list | None = None
    ) -> dict:
        """Async version of get_customer."""
        url = f"{self.crm_url}/api/v4/customers/{customer_id}"
        if with_params:
            url += "?with=" + ",".join(param for param in with_params)
        return await self._send_api_request_async("get", url)

    async def create_customers_async(self, customers: list) -> dict:
        """Async version of create_customers."""
        return await self._create_or_update_entities_async("customers", customers)

    async def update_customers_async(self, customers: list) -> dict:
        """Async version of update_customers."""
        return await self._create_or_update_entities_async("customers", customers, True)

    async def get_transactions_async(
        self,
        customer_id: int | None = None,
        limit: int = 250,
        page: int = 1,
        filter_by_ids: int | list | None = None,
    ) -> dict:
        """Async version of get_transactions."""
        url = (
            f"{self.crm_url}/api/v4/customers/{customer_id}/transactions"
            if customer_id is not None
            else f"{self.crm_url}/api/v4/customers/transactions"
        )
        params: dict = {"limit": limit, "page": page}
        if filter_by_ids:
            params["filter[id][]" if isinstance(filter_by_ids, list) else "filter[id]"] = (
                filter_by_ids
            )
        return await self._send_api_request_async(
            "get", f"{url}?{urlencode(params, doseq=True)}"
        )

    async def get_transaction_async(
        self, transaction_id: int, customer_id: int | None = None
    ) -> dict:
        """Async version of get_transaction."""
        url = (
            f"{self.crm_url}/api/v4/customers/{customer_id}/transactions/{transaction_id}"
            if customer_id is not None
            else f"{self.crm_url}/api/v4/customers/transactions/{transaction_id}"
        )
        return await self._send_api_request_async("get", url)

    async def create_transactions_async(
        self, customer_id: int, transactions: list
    ) -> dict:
        """Async version of create_transactions."""
        url = f"{self.crm_url}/api/v4/customers/{customer_id}/transactions"
        return await self._send_api_request_async("post", url, transactions)

    async def delete_transaction_async(
        self, transaction_id: int, customer_id: int | None = None
    ) -> dict:
        """Async version of delete_transaction."""
        url = (
            f"{self.crm_url}/api/v4/customers/{customer_id}/transactions/{transaction_id}"
            if customer_id is not None
            else f"{self.crm_url}/api/v4/customers/transactions/{transaction_id}"
        )
        return await self._send_api_request_async("delete", url)

    async def change_bonus_points_async(
        self, customer_id: int, points: dict
    ) -> dict:
        """Async version of change_bonus_points."""
        url = f"{self.crm_url}/api/v4/customers/{customer_id}/bonus_points"
        return await self._send_api_request_async("post", url, points)
