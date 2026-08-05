from urllib.parse import urlencode

from .base import Entity


class ChatTemplates(Entity):
    def _build_get_chat_templates_url(
        self,
        page: int,
        limit: int,
        filter_by_external_ids: str | int | bool | list | None,
        with_params: list | None,
    ) -> str:
        url = f"{self.crm_url}/api/v4/chats/templates"
        params: dict = {"page": page, "limit": limit}
        if with_params:
            params["with"] = ",".join(param for param in with_params)
        if filter_by_external_ids:
            params[
                "filter[external_id][]"
                if isinstance(filter_by_external_ids, list)
                else "filter[external_id]"
            ] = filter_by_external_ids
        return f"{url}?{urlencode(params, doseq=True)}"

    def _build_get_chat_template_url(
        self, template_id: int, with_params: list | None
    ) -> str:
        url = f"{self.crm_url}/api/v4/chats/templates/{template_id}"
        if with_params:
            url += "?with=" + ",".join(param for param in with_params)
        return url

    def get_chat_templates(
        self,
        page: int = 1,
        limit: int = 50,
        filter_by_external_ids: str | int | bool | list | None = None,
        with_params: list | None = None,
    ) -> dict:
        """Get chat templates list
        Doc: https://www.amocrm.ru/developers/content/crm_platform/chat-templates-api
        Args:
            page (int, optional): page number. Defaults to 1.
            limit (int, optional): limit per page. Defaults to 50.
            filter_by_external_ids (Union[str, int, bool, list, None], optional): external ids filter. Defaults to None.
            with_params (Optional[list], optional): with params (reviews). Defaults to None.

        Returns:
            dict: list of chat templates
        """
        url = self._build_get_chat_templates_url(
            page, limit, filter_by_external_ids, with_params
        )
        return self._send_api_request("get", url)

    def get_chat_template(
        self, template_id: int, with_params: list | None = None
    ) -> dict:
        """Get chat template by id
        Doc: https://www.amocrm.ru/developers/content/crm_platform/chat-templates-api
        Args:
            template_id (int): template id
            with_params (Optional[list], optional): with params (reviews). Defaults to None.

        Returns:
            dict: chat template model
        """
        url = self._build_get_chat_template_url(template_id, with_params)
        return self._send_api_request("get", url)

    def create_chat_templates(self, templates: list) -> dict:
        """Create chat templates
        Doc: https://www.amocrm.ru/developers/content/crm_platform/chat-templates-api
        Args:
            templates (list): list of templates

        Returns:
            dict: created templates
        """
        url = f"{self.crm_url}/api/v4/chats/templates"
        return self._send_api_request("post", url, templates)

    def update_chat_templates(self, templates: list) -> dict:
        """Update chat templates in batch
        Doc: https://www.amocrm.ru/developers/content/crm_platform/chat-templates-api
        Args:
            templates (list): list of templates with ids

        Returns:
            dict: updated templates
        """
        url = f"{self.crm_url}/api/v4/chats/templates"
        return self._send_api_request("patch", url, templates)

    def update_chat_template(self, template_id: int, template: dict) -> dict:
        """Update single chat template
        Doc: https://www.amocrm.ru/developers/content/crm_platform/chat-templates-api
        Args:
            template_id (int): template id
            template (dict): template model

        Returns:
            dict: updated template
        """
        url = f"{self.crm_url}/api/v4/chats/templates/{template_id}"
        return self._send_api_request("patch", url, template)

    def delete_chat_templates(self, templates: list | None = None) -> dict:
        """Delete chat templates
        Doc: https://www.amocrm.ru/developers/content/crm_platform/chat-templates-api
        Args:
            templates (Optional[list], optional): list of templates with ids. Defaults to None.

        Returns:
            dict: empty response
        """
        url = f"{self.crm_url}/api/v4/chats/templates"
        return self._send_api_request("delete", url, templates)

    def delete_chat_template(self, template_id: int) -> dict:
        """Delete single chat template
        Doc: https://www.amocrm.ru/developers/content/crm_platform/chat-templates-api
        Args:
            template_id (int): template id

        Returns:
            dict: empty response
        """
        url = f"{self.crm_url}/api/v4/chats/templates/{template_id}"
        return self._send_api_request("delete", url)

    def send_chat_template_to_review(self, template_id: int) -> dict:
        """Send WhatsApp template to moderation
        Doc: https://www.amocrm.ru/developers/content/crm_platform/chat-templates-api
        Args:
            template_id (int): template id

        Returns:
            dict: reviews
        """
        url = f"{self.crm_url}/api/v4/chats/templates/{template_id}/review"
        return self._send_api_request("post", url, {})

    def update_chat_template_review_status(
        self,
        template_id: int,
        review_id: int,
        status: str,
        reject_reason: str | None = None,
    ) -> dict:
        """Update WhatsApp template review status
        Doc: https://www.amocrm.ru/developers/content/crm_platform/chat-templates-api
        Args:
            template_id (int): template id
            review_id (int): review id
            status (str): approved, paused or rejected
            reject_reason (Optional[str], optional): rejection reason. Defaults to None.

        Returns:
            dict: updated review
        """
        url = (
            f"{self.crm_url}/api/v4/chats/templates/{template_id}/review/{review_id}"
        )
        params = {"status": status}
        if reject_reason is not None:
            params["reject_reason"] = reject_reason
        return self._send_api_request("post", url, params)

    async def get_chat_templates_async(
        self,
        page: int = 1,
        limit: int = 50,
        filter_by_external_ids: str | int | bool | list | None = None,
        with_params: list | None = None,
    ) -> dict:
        """Async version of get_chat_templates."""
        url = self._build_get_chat_templates_url(
            page, limit, filter_by_external_ids, with_params
        )
        return await self._send_api_request_async("get", url)

    async def get_chat_template_async(
        self, template_id: int, with_params: list | None = None
    ) -> dict:
        """Async version of get_chat_template."""
        url = self._build_get_chat_template_url(template_id, with_params)
        return await self._send_api_request_async("get", url)

    async def create_chat_templates_async(self, templates: list) -> dict:
        """Async version of create_chat_templates."""
        url = f"{self.crm_url}/api/v4/chats/templates"
        return await self._send_api_request_async("post", url, templates)

    async def update_chat_templates_async(self, templates: list) -> dict:
        """Async version of update_chat_templates."""
        url = f"{self.crm_url}/api/v4/chats/templates"
        return await self._send_api_request_async("patch", url, templates)

    async def update_chat_template_async(
        self, template_id: int, template: dict
    ) -> dict:
        """Async version of update_chat_template."""
        url = f"{self.crm_url}/api/v4/chats/templates/{template_id}"
        return await self._send_api_request_async("patch", url, template)

    async def delete_chat_templates_async(
        self, templates: list | None = None
    ) -> dict:
        """Async version of delete_chat_templates."""
        url = f"{self.crm_url}/api/v4/chats/templates"
        return await self._send_api_request_async("delete", url, templates)

    async def delete_chat_template_async(self, template_id: int) -> dict:
        """Async version of delete_chat_template."""
        url = f"{self.crm_url}/api/v4/chats/templates/{template_id}"
        return await self._send_api_request_async("delete", url)

    async def send_chat_template_to_review_async(self, template_id: int) -> dict:
        """Async version of send_chat_template_to_review."""
        url = f"{self.crm_url}/api/v4/chats/templates/{template_id}/review"
        return await self._send_api_request_async("post", url, {})

    async def update_chat_template_review_status_async(
        self,
        template_id: int,
        review_id: int,
        status: str,
        reject_reason: str | None = None,
    ) -> dict:
        """Async version of update_chat_template_review_status."""
        url = (
            f"{self.crm_url}/api/v4/chats/templates/{template_id}/review/{review_id}"
        )
        params = {"status": status}
        if reject_reason is not None:
            params["reject_reason"] = reject_reason
        return await self._send_api_request_async("post", url, params)
