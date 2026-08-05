from .base import Entity


class CustomerStatuses(Entity):
    def get_customer_statuses(self) -> dict:
        """Get customer statuses
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-statuses-api#customers-statuses-list
        Returns:
            dict: list of customer statuses
        """
        url = f"{self.crm_url}/api/v4/customers/statuses"
        return self._send_api_request("get", url)

    def get_customer_status(self, status_id: int) -> dict:
        """Get customer status by id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-statuses-api#customer-status-detail
        Args:
            status_id (int): status id

        Returns:
            dict: customer status model
        """
        url = f"{self.crm_url}/api/v4/customers/statuses/{status_id}"
        return self._send_api_request("get", url)

    def create_customer_statuses(self, statuses: list) -> dict:
        """Create customer statuses
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-statuses-api#customers-statuses-add
        Args:
            statuses (list): list of statuses

        Returns:
            dict: created statuses
        """
        url = f"{self.crm_url}/api/v4/customers/statuses"
        return self._send_api_request("post", url, statuses)

    def update_customer_status(self, status_id: int, params: dict) -> dict:
        """Update customer status
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-statuses-api#customers-status-edit
        Args:
            status_id (int): status id
            params (dict): status params to update

        Returns:
            dict: updated status
        """
        url = f"{self.crm_url}/api/v4/customers/statuses/{status_id}"
        return self._send_api_request("patch", url, params)

    def delete_customer_status(self, status_id: int) -> dict:
        """Delete customer status
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-statuses-api#customer-status-delete
        Args:
            status_id (int): status id

        Returns:
            dict: empty response
        """
        url = f"{self.crm_url}/api/v4/customers/statuses/{status_id}"
        return self._send_api_request("delete", url)

    def get_customer_segments(
        self, page: int = 1, limit: int = 250
    ) -> dict:
        """Get customer segments
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-statuses-api#segments-list
        Args:
            page (int, optional): page number. Defaults to 1.
            limit (int, optional): limit per page. Defaults to 250.

        Returns:
            dict: list of customer segments
        """
        url = (
            f"{self.crm_url}/api/v4/customers/segments?page={page}&limit={limit}"
        )
        return self._send_api_request("get", url)

    def get_customer_segment(self, segment_id: int) -> dict:
        """Get customer segment by id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-statuses-api#segment-detail
        Args:
            segment_id (int): segment id

        Returns:
            dict: customer segment model
        """
        url = f"{self.crm_url}/api/v4/customers/segments/{segment_id}"
        return self._send_api_request("get", url)

    def create_customer_segment(self, segment: dict) -> dict:
        """Create customer segment
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-statuses-api#segment-add
        Args:
            segment (dict): segment model

        Returns:
            dict: created segment
        """
        url = f"{self.crm_url}/api/v4/customers/segments"
        return self._send_api_request("post", url, segment)

    def update_customer_segment(self, segment_id: int, params: dict) -> dict:
        """Update customer segment
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-statuses-api#segment-edit
        Args:
            segment_id (int): segment id
            params (dict): segment params to update

        Returns:
            dict: updated segment
        """
        url = f"{self.crm_url}/api/v4/customers/segments/{segment_id}"
        return self._send_api_request("patch", url, params)

    def delete_customer_segment(self, segment_id: int) -> dict:
        """Delete customer segment
        Doc: https://www.amocrm.ru/developers/content/crm_platform/customers-statuses-api#segment-delete
        Args:
            segment_id (int): segment id

        Returns:
            dict: empty response
        """
        url = f"{self.crm_url}/api/v4/customers/segments/{segment_id}"
        return self._send_api_request("delete", url)

    async def get_customer_statuses_async(self) -> dict:
        """Async version of get_customer_statuses."""
        url = f"{self.crm_url}/api/v4/customers/statuses"
        return await self._send_api_request_async("get", url)

    async def get_customer_status_async(self, status_id: int) -> dict:
        """Async version of get_customer_status."""
        url = f"{self.crm_url}/api/v4/customers/statuses/{status_id}"
        return await self._send_api_request_async("get", url)

    async def create_customer_statuses_async(self, statuses: list) -> dict:
        """Async version of create_customer_statuses."""
        url = f"{self.crm_url}/api/v4/customers/statuses"
        return await self._send_api_request_async("post", url, statuses)

    async def update_customer_status_async(
        self, status_id: int, params: dict
    ) -> dict:
        """Async version of update_customer_status."""
        url = f"{self.crm_url}/api/v4/customers/statuses/{status_id}"
        return await self._send_api_request_async("patch", url, params)

    async def delete_customer_status_async(self, status_id: int) -> dict:
        """Async version of delete_customer_status."""
        url = f"{self.crm_url}/api/v4/customers/statuses/{status_id}"
        return await self._send_api_request_async("delete", url)

    async def get_customer_segments_async(
        self, page: int = 1, limit: int = 250
    ) -> dict:
        """Async version of get_customer_segments."""
        url = (
            f"{self.crm_url}/api/v4/customers/segments?page={page}&limit={limit}"
        )
        return await self._send_api_request_async("get", url)

    async def get_customer_segment_async(self, segment_id: int) -> dict:
        """Async version of get_customer_segment."""
        url = f"{self.crm_url}/api/v4/customers/segments/{segment_id}"
        return await self._send_api_request_async("get", url)

    async def create_customer_segment_async(self, segment: dict) -> dict:
        """Async version of create_customer_segment."""
        url = f"{self.crm_url}/api/v4/customers/segments"
        return await self._send_api_request_async("post", url, segment)

    async def update_customer_segment_async(
        self, segment_id: int, params: dict
    ) -> dict:
        """Async version of update_customer_segment."""
        url = f"{self.crm_url}/api/v4/customers/segments/{segment_id}"
        return await self._send_api_request_async("patch", url, params)

    async def delete_customer_segment_async(self, segment_id: int) -> dict:
        """Async version of delete_customer_segment."""
        url = f"{self.crm_url}/api/v4/customers/segments/{segment_id}"
        return await self._send_api_request_async("delete", url)
