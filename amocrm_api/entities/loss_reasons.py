from urllib.parse import urlencode

from .base import Entity


class LossReasons(Entity):
    def _build_get_loss_reasons_url(
        self, page: int, limit: int, with_params: list | None
    ) -> str:
        url = f"{self.crm_url}/api/v4/leads/loss_reasons"
        params: dict = {"page": page, "limit": limit}
        if with_params:
            params["with"] = ",".join(param for param in with_params)
        return f"{url}?{urlencode(params)}"

    def _build_get_loss_reason_url(self, loss_reason_id: int) -> str:
        return f"{self.crm_url}/api/v4/leads/loss_reasons/{loss_reason_id}"

    def get_loss_reasons(
        self,
        page: int = 1,
        limit: int = 250,
        with_params: list | None = None,
    ) -> dict:
        """Get loss reasons
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads-api#loss-reasons-list
        Args:
            page (int, optional): number of page. Defaults to 1.
            limit (int, optional): limit rows. Defaults to 250.
            with_params (Optional[list], optional): with params. Defaults to None.
        """
        url = self._build_get_loss_reasons_url(page, limit, with_params)
        return self._send_api_request("get", url)

    def get_loss_reason(self, loss_reason_id: int) -> dict:
        """Get loss reason by id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads-api#loss-reasons-detail
        Args:
            loss_reason_id (int): id of loss reason
        """
        url = self._build_get_loss_reason_url(loss_reason_id)
        return self._send_api_request("get", url)

    def create_loss_reasons(self, loss_reasons: list) -> dict:
        """Create loss reasons
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads-api#loss-reasons-add
        Args:
            loss_reasons (list): list of loss reasons
        """
        url = f"{self.crm_url}/api/v4/leads/loss_reasons"
        return self._send_api_request("post", url, loss_reasons)

    def update_loss_reasons(self, loss_reasons: list) -> dict:
        """Update loss reasons
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads-api#loss-reasons-edit
        Args:
            loss_reasons (list): list of loss reasons with ids
        """
        url = f"{self.crm_url}/api/v4/leads/loss_reasons"
        return self._send_api_request("patch", url, loss_reasons)

    def delete_loss_reason(self, loss_reason_id: int) -> dict:
        """Delete loss reason by id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/leads-api#loss-reasons-delete
        Args:
            loss_reason_id (int): id of loss reason
        """
        url = self._build_get_loss_reason_url(loss_reason_id)
        return self._send_api_request("delete", url)

    async def get_loss_reasons_async(
        self,
        page: int = 1,
        limit: int = 250,
        with_params: list | None = None,
    ) -> dict:
        """Async version of get_loss_reasons."""
        url = self._build_get_loss_reasons_url(page, limit, with_params)
        return await self._send_api_request_async("get", url)

    async def get_loss_reason_async(self, loss_reason_id: int) -> dict:
        """Async version of get_loss_reason."""
        url = self._build_get_loss_reason_url(loss_reason_id)
        return await self._send_api_request_async("get", url)

    async def create_loss_reasons_async(self, loss_reasons: list) -> dict:
        """Async version of create_loss_reasons."""
        url = f"{self.crm_url}/api/v4/leads/loss_reasons"
        return await self._send_api_request_async("post", url, loss_reasons)

    async def update_loss_reasons_async(self, loss_reasons: list) -> dict:
        """Async version of update_loss_reasons."""
        url = f"{self.crm_url}/api/v4/leads/loss_reasons"
        return await self._send_api_request_async("patch", url, loss_reasons)

    async def delete_loss_reason_async(self, loss_reason_id: int) -> dict:
        """Async version of delete_loss_reason."""
        url = self._build_get_loss_reason_url(loss_reason_id)
        return await self._send_api_request_async("delete", url)
